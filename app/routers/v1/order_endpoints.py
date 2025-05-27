import os
import uuid

from fastapi import APIRouter, Depends, Path, Query, status, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, models, log, cruds
from app.dependencies.db_session import get_db
from app.core.config import settings
from app.core import enums, exceptions

router = APIRouter(tags=["Orders"])


@router.get("/partners/{partnerId}/network/order")
async def get_multi(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    db_objs, total_count = cruds.order_cruds.get_multi(
        db=db, page=page, page_size=page_size
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "records": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
            "total_count": total_count,
        },
    )


@router.get("/partners/{partnerId}/network/order/{orderId}")
async def get(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    order_id: uuid.UUID = Path(alias="orderId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.order_cruds.get_by_order_id(db=db, order_id=order_id)
    if not db_obj:
        err = f"Order {order_id} does not exist"
        raise exceptions.NotFoundError(err)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj.to_schema()),
    )


@router.post("/partners/{partnerId}/network/order/upload")
async def upload(
    file: UploadFile = File(...),
    api_name: enums.ApiNameEnums = Query(alias="apiName"),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        err = "Un supported file format"
        raise exceptions.BadRequestError(err)

    order_id = uuid.uuid4()
    os.makedirs(settings.ORDER_STORAGE_PATH, exist_ok=True)
    file_name = f"{order_id}.csv"
    full_file_path = os.path.join(settings.ORDER_STORAGE_PATH, file_name)

    with open(full_file_path, "wb") as f:
        f.write(file.file.read())

    order_create_data = schemas.OrderCreate.model_validate(
        {
            "file_name": file_name,
            "api_name": api_name,
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


@router.get("/partners/{partnerId}/network/order/download/{orderId}")
async def download(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    order_id: uuid.UUID = Path(alias="orderId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.order_cruds.get_by_order_id(db=db, order_id=order_id)
    if not db_obj:
        err = f"Order {order_id} does not exist"
        raise exceptions.NotFoundError(err)

    file_path = f"{settings.ORDER_STORAGE_PATH}/{db_obj.file_name}"
    return FileResponse(
        path=file_path,
        filename=db_obj.file_name,
        media_type="application/octet-stream",
    )
