import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, log, cruds
from app.dependencies.db_session import get_db
from app.services import comcast_integration
from app.core import exceptions, enums

router = APIRouter(tags=["Site Intent APIs"])


@router.post("/partners/{partnerId}/network/siteIntent")
async def create(
    data_in: schemas.SiteIntentCreate,
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
):
    site_intent_id = uuid.uuid4()
    db_obj = cruds.site_intent_cruds.create(
        db=db, data_in=data_in, site_intent_id=site_intent_id
    )

    log.info(f"Site intent draft created in db with draft id {db_obj.site_intent_id}")

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(db_obj.to_schema()),
    )


@router.get("/partners/{partnerId}/network/siteIntent")
def get_multi(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    db_objs, total_count = cruds.site_intent_cruds.get_multi(
        db=db, page=page, page_size=page_size
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "records": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
            "total_count": total_count,
        },
    )


@router.delete("/partners/{partnerId}/network/siteIntent/{siteIntentId}")
def delete(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    site_intent_id: uuid.UUID = Path(alias="siteIntentId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.site_intent_cruds.get_by_site_intent_id(
        db=db, site_intent_id=site_intent_id
    )

    if not db_obj:
        err = f"Site intent {site_intent_id} does not exist"
        raise exceptions.NotFoundError(err)

    if not db_obj.is_draft:
        log.info(f"Deleting the site intent {site_intent_id} over comcast")
        try:
            comcast_integration.SiteIntentIntegration(partner_id=partner_id).delete(
                site_intent_id=site_intent_id
            )
        except exceptions.NotFoundError:
            raise

        except Exception as err:
            raise exceptions.BackendError(err)

    cruds.site_intent_cruds.delete(db=db, db_obj=db_obj)

    log.info(f"Site intent {site_intent_id} deleted from db")

    return status.HTTP_204_NO_CONTENT


@router.put("/partners/{partnerId}/network/siteIntent/{siteIntentId}:push")
def push_to_comcast(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    site_intent_id: uuid.UUID = Path(alias="siteIntentId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.site_intent_cruds.get_by_site_intent_id(
        db=db, site_intent_id=site_intent_id
    )

    if not db_obj:
        err = f"Site intent {site_intent_id} does not exist"
        raise exceptions.NotFoundError(err)

    if not db_obj.is_draft:
        err = f"Site intent id {site_intent_id} already pushed to comcast"
        raise exceptions.ConflictError(err)

    db_data = jsonable_encoder(db_obj.to_schema())
    comcast_input = {
        "siteIntentName": db_data.get("siteIntentName"),
        "refHubName": db_data.get("refHubName"),
        "refHubId": db_data.get("refHubId"),
        "csvIpOob": db_data.get("csvIpOob"),
    }

    try:
        comcast_response = comcast_integration.SiteIntentIntegration(
            partner_id=partner_id
        ).create(data=comcast_input)
    except exceptions.NotFoundError:
        raise

    except Exception as err:
        raise exceptions.BackendError(err)

    transaction_id = uuid.uuid4()
    transaction_create_data = schemas.TransactionCreate.model_validate(
        {
            "transaction_status": enums.TransactionStatus.COMPLETED,
            "transaction_type": enums.TransactionType.SINGLE,
            "message": "na",
        },
        by_name=True,
    )
    db_ob_transaction = cruds.transaction_cruds.create(
        db=db, data_in=transaction_create_data, transaction_id=transaction_id
    )

    db_obj = cruds.site_intent_cruds.push(
        db=db,
        db_obj=db_obj,
        site_intent_id=comcast_response.get("siteIntentId"),
        transaction_id=db_ob_transaction.transaction_id,
    )

    log.info(f"Site intent {site_intent_id} record from comcast updated in db")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj.to_schema()),
    )
