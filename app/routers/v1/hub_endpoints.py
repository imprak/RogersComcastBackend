import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import schemas, models, log, cruds
from app.dependencies.db_session import get_db

router = APIRouter(tags=["ISP APIs"])


@router.post("/partners/{partnerId}/network/hub")
async def create(
    data_in: schemas.HubCreate,
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
):

    parent_hub_name = data_in.ref_parent_hub_name
    db_obj = cruds.hub_cruds.create(
        db=db, data=data_in, parent_hub_name=parent_hub_name
    )

    JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=db_obj.to_schema(),
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
        content=[db_obj.to_schema() for db_obj in db_objs],
    )


@router.delete("/partners/{partnerId}/network/hub/{hubId}")
def delete(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    hub_id: str = Query(alias="hubId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.hub_cruds.get_by_hub_id(db=db, hub_id=hub_id)

    if not db_obj:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "not found"},
        )
    cruds.hub_cruds.delete(db=db, db_obj=db_obj)

    return status.HTTP_204_NO_CONTENT


@router.put("/partners/{partnerId}/network/hub/{hubId}/launch")
def launch_to_comcast(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    hub_id: str = Query(alias="hubId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.hub_cruds.get(db=db, hub_id=hub_id)

    if not db_obj:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "not found"},
        )

    hub_id = hub_id
    db_obj = cruds.hub_cruds.launch(db=db, hub_id=hub_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=db_obj.to_schema(),
    )
