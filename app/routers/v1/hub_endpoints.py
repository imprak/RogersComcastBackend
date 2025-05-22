import io
import os
import uuid

from fastapi import APIRouter, Depends, Path, Query, status, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, models, log, cruds
from app.dependencies.db_session import get_db
from app.utils.comcast_integration import HubIntegration
from app.core import enums
from app.core.config import settings

router = APIRouter(tags=["Hub APIs"])


@router.post("/partners/{partnerId}/network/hub")
async def create(
    data_in: schemas.HubCreate,
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
):
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

    parent_hub_name = data_in.ref_parent_hub_name
    hub_id = uuid.uuid4()
    db_obj = cruds.hub_cruds.create(
        db=db,
        data_in=data_in,
        parent_hub_name=parent_hub_name,
        transaction_id=db_ob_transaction.transaction_id,
        hub_id=hub_id,
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(db_obj.to_schema()),
    )


@router.get("/partners/{partnerId}/network/hub")
def get_multi(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    db_objs = cruds.hub_cruds.get_multi(db=db, page=page, page_size=page_size)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
    )


@router.delete("/partners/{partnerId}/network/hub/{hubId}")
def delete(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    hub_id: uuid.UUID = Query(alias="hubId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.hub_cruds.get_by_hub_id(db=db, hub_id=hub_id)

    if not db_obj:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "not found"},
        )

    if not db_obj.is_draft:
        HubIntegration(partner_id=partner_id).delete(hub_id=hub_id)

    cruds.hub_cruds.delete(db=db, db_obj=db_obj)

    return status.HTTP_204_NO_CONTENT


@router.put("/partners/{partnerId}/network/hub/{hubId}:push")
def push_to_comcast(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    hub_id: uuid.UUID = Query(alias="hubId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.hub_cruds.get_by_hub_id(db=db, hub_id=hub_id)

    if not db_obj:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "not found"},
        )

    if not db_obj.is_draft:
        err = f"Site intent id {hub_id} already pushed to comcast"
        log.error(err)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"message": err}
        )

    comcast_response = HubIntegration(partner_id=partner_id).create(db_obj)
    db_obj = cruds.hub_cruds.push(
        db=db, db_obj=db_obj, hub_id=comcast_response.get("hub_id")
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj.to_schema()),
    )


@router.post("/partners/{partnerId}/network/hub/upload-order")
async def upload_order(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        err = "Un supported file format"
        log.error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": err}
        )

    content = await file.read()
    order_id = uuid.uuid4()

    os.makedirs(settings.ORDER_STORAGE_PATH, exist_ok=True)
    file_name = f"{order_id}.csv"
    full_file_path = f"{settings.ORDER_STORAGE_PATH}/{file_name}"

    with open(full_file_path, "w+") as f:
        f.write(content.decode("utf-8"))

    transaction_id = uuid.uuid4()
    transaction_create_data = schemas.TransactionCreate.model_validate(
        {
            "transaction_status": enums.TransactionStatus.IN_PROGRESS,
            "transaction_type": enums.TransactionType.BULK,
            "message": "under validation",
        },
        by_name=True,
    )
    db_ob_transaction = cruds.transaction_cruds.create(
        db=db, data_in=transaction_create_data, transaction_id=transaction_id
    )

    order_create_data = schemas.OrderCreate.model_validate(
        {
            "file_name": file_name,
            "transaction_id": db_ob_transaction.transaction_id,
            "order_status": enums.OrderStatus.IN_PROGRESS,
            "message": "under validation",
        },
        by_name=True,
    )
    db_obj_order = cruds.order_cruds.create(
        db=db, data_in=order_create_data, order_id=order_id
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj_order.to_schema()),
    )
