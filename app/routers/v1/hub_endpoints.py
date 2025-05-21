import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, models, log, cruds
from app.dependencies.db_session import get_db
from app.utils.comcast_integration import HubIntegration

router = APIRouter(tags=["Hub APIs"])


@router.post("/partners/{partnerId}/network/hub")
async def create(
    data_in: schemas.HubCreate,
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
):

    parent_hub_name = data_in.ref_parent_hub_name
    db_obj = cruds.hub_cruds.create(
        db=db, data_in=data_in, parent_hub_name=parent_hub_name
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
