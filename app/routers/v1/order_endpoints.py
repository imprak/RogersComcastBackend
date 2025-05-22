import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, models, log, cruds
from app.dependencies.db_session import get_db

router = APIRouter(tags=["Transaction& & Orders"])


@router.get("/partners/{partnerId}/network/order")
async def get_multi(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    db_objs = cruds.order_cruds.get_multi(db=db, page=page, page_size=page_size)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
    )


@router.get("/partners/{partnerId}/network/order/{orderId}")
async def get(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    order_id: uuid.UUID = Path(alias="orderId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.order_cruds.get_by_order_id(db=db, order_id=order_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj.to_schema()),
    )
