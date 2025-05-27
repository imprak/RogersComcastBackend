import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, log, cruds
from app.dependencies.db_session import get_db
from app.services import comcast_integration
from app.core import exceptions, enums

router = APIRouter(tags=["Ppod Intent APIs"])


@router.post("/partners/{partnerId}/network/ppodIntent")
async def create(
    data_in: schemas.PpodIntentCreate,
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
):
    ppod_intent_id = uuid.uuid4()
    db_obj = cruds.ppod_intent_cruds.create(
        db=db, data_in=data_in, ppod_intent_id=ppod_intent_id
    )

    log.info(f"Ppod intent draft created in db with draft id {db_obj.ppod_intent_id}")

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(db_obj.to_schema()),
    )


@router.get("/partners/{partnerId}/network/ppodIntent")
def get_multi(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    db_objs, total_count = cruds.ppod_intent_cruds.get_multi(
        db=db, page=page, page_size=page_size
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "records": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
            "total_count": total_count,
        },
    )


@router.delete("/partners/{partnerId}/network/ppodIntent/{ppodIntentId}")
def delete(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    ppod_intent_id: uuid.UUID = Path(alias="ppodIntentId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.ppod_intent_cruds.get_by_ppod_intent_id(
        db=db, ppod_intent_id=ppod_intent_id
    )

    if not db_obj:
        err = f"Ppod intent {ppod_intent_id} does not exist"
        raise exceptions.NotFoundError(err)

    if not db_obj.is_draft:
        log.info(f"Deleting the ppod intent {ppod_intent_id} over comcast")
        try:
            comcast_integration.PpodIntentIntegration(partner_id=partner_id).delete(
                ppod_intent_id=ppod_intent_id
            )
        except exceptions.NotFoundError:
            raise

        except Exception as err:
            raise exceptions.BackendError(err)

    cruds.ppod_intent_cruds.delete(db=db, db_obj=db_obj)

    log.info(f"Ppod intent {ppod_intent_id} deleted from db")

    return status.HTTP_204_NO_CONTENT


@router.put("/partners/{partnerId}/network/ppodIntent/{ppodIntentId}:push")
def push_to_comcast(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    ppod_intent_id: uuid.UUID = Path(alias="ppodIntentId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.ppod_intent_cruds.get_by_ppod_intent_id(
        db=db, ppod_intent_id=ppod_intent_id
    )

    if not db_obj:
        err = f"Ppod intent {ppod_intent_id} does not exist"
        raise exceptions.NotFoundError(err)

    if not db_obj.is_draft:
        err = f"Ppod intent id {ppod_intent_id} already pushed to comcast"
        raise exceptions.ConflictError(err)

    db_data = jsonable_encoder(db_obj.to_schema())
    comcast_input = {
        "ppodIntentName": db_data.get("ppodIntentName"),
        "refCpodIntentName": db_data.get("refCpodIntentName"),
        "refCpodIntentId": str(db_obj.ref_cpod_intent_id),
    }

    try:
        comcast_response = comcast_integration.PpodIntentIntegration(
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

    db_obj = cruds.ppod_intent_cruds.push(
        db=db,
        db_obj=db_obj,
        transaction_id=db_ob_transaction.transaction_id,
        ppod_intent_id=comcast_response.get("ppodIntentId"),
        cpod_intent_id=comcast_response.get("cpodIntentId"),
    )

    log.info(f"Ppod intent {ppod_intent_id} record from comcast updated in db")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj.to_schema()),
    )
