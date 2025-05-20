import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import schemas, models, log, cruds
from app.dependencies.db_session import get_db

router = APIRouter(tags=["Home Screen"])


@router.post("/partners/{partnerId}/network/apis")
async def create(
    data_in: schemas.ApiCreate,
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
):

    api_id = uuid.uuid4()
    db_obj = cruds.api_cruds.create(db=db, data=data_in, api_id=api_id)

    JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=db_obj.to_schema(),
    )


@router.get("/partners/{partnerId}/network/apis")
def get_multi(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    db_objs = cruds.api_cruds.get_multi(db=db, page=page, page_size=page_size)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[db_obj.to_schema() for db_obj in db_objs],
    )


@router.delete("/partners/{partnerId}/network/api/apiId")
def delete(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    api_id: str = Query(alias="apiId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.api_cruds.get_by_api_id(db=db, api_id=api_id)

    if not db_obj:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "not found"},
        )
    cruds.hub_cruds.delete(db=db, db_obj=db_obj)

    return status.HTTP_204_NO_CONTENT
