import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, models, log, cruds
from app.dependencies.db_session import get_db
from app.core import exceptions

router = APIRouter(tags=["Transactions"])


@router.get("/partners/{partnerId}/network/transaction")
async def get_multi(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    db_objs, total_count = cruds.transaction_cruds.get_multi(
        db=db, page=page, page_size=page_size
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "records": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
            "total_count": total_count,
        },
    )


@router.get("/partners/{partnerId}/network/transaction/{transactionId}")
async def get(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    transaction_id: uuid.UUID = Path(alias="transactionId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.transaction_cruds.get_by_transaction_id(
        db=db, transaction_id=transaction_id
    )

    if not db_obj:
        err = f"Transaction {transaction_id} does not exist"
        raise exceptions.NotFoundError(err)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj.to_schema()),
    )
