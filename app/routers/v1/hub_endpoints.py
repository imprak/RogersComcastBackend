import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, log, cruds
from app.dependencies.db_session import get_db
from app.services.comcast_integration import HubIntegration
from app.core import enums, exceptions
from app.core.config import settings

router = APIRouter(tags=["Hub APIs"])


@router.get("/partners/{partnerId}/network/hub")
def get_multi(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    db_objs, total_count = cruds.hub_cruds.get_multi(
        db=db, page=page, page_size=page_size
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "records": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
            "total_count": total_count,
        },
    )


@router.post("/partners/{partnerId}/network/hub")
async def create(
    data_in: schemas.HubCreate,
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
):

    parent_hub_name = data_in.ref_parent_hub_name
    hub_id = uuid.uuid4()
    db_obj = cruds.hub_cruds.create(
        db=db,
        hub_id=hub_id,
        data_in=data_in,
        parent_hub_name=parent_hub_name,
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(db_obj.to_schema()),
    )


@router.patch("/partners/{partnerId}/network/hub/{hubId}")
def update(
    data_in: schemas.HubUpdate,
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    hub_id: uuid.UUID = Path(alias="hubId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.hub_cruds.get_by_hub_id(db=db, hub_id=hub_id)

    if not db_obj:
        err = f"Hub {hub_id} does not exist"
        raise exceptions.NotFoundError(err)

    db_obj = cruds.hub_cruds.update(db=db, db_obj=db_obj, data_in=data_in)

    if not db_obj.is_draft:
        HubIntegration(partner_id=partner_id).update(
            hub_id=hub_id, data=db_obj.to_schema()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj.to_schema()),
    )


@router.delete("/partners/{partnerId}/network/hub/{hubId}")
def delete(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    hub_id: uuid.UUID = Path(alias="hubId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.hub_cruds.get_by_hub_id(db=db, hub_id=hub_id)

    if not db_obj:
        err = f"Hub {hub_id} does not exist"
        raise exceptions.NotFoundError(err)

    if not db_obj.is_draft:
        HubIntegration(partner_id=partner_id).delete(hub_id=hub_id)

    cruds.hub_cruds.delete(db=db, db_obj=db_obj)

    return status.HTTP_204_NO_CONTENT


@router.put("/partners/{partnerId}/network/hub/{hubId}:push")
def push_to_comcast(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    hub_id: uuid.UUID = Path(alias="hubId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.hub_cruds.get_by_hub_id(db=db, hub_id=hub_id)

    if not db_obj:
        err = f"Hub {hub_id} does not exist"
        raise exceptions.NotFoundError(err)

    if not db_obj.is_draft:
        err = f"Hub {hub_id} already pushed to comcast"
        raise exceptions.ConflictError(err)

    comcast_response = HubIntegration(partner_id=partner_id).create(db_obj)

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

    db_obj = cruds.hub_cruds.push(
        db=db,
        db_obj=db_obj,
        hub_id=comcast_response.get("hub_id"),
        transaction_id=db_ob_transaction.transaction_id,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj.to_schema()),
    )
