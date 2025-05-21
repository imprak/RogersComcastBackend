import uuid

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, models, log, cruds
from app.dependencies.db_session import get_db
from app.utils import comcast_integration

router = APIRouter(tags=["Site Intent APIs"])


@router.post("/partners/{partnerId}/network/siteIntent")
async def create(
    data_in: schemas.SiteIntentCreate,
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.site_intent_cruds.create(db=db, data_in=data_in)

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
    db_objs = cruds.site_intent_cruds.get_multi(db=db, page=page, page_size=page_size)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
    )


@router.delete("/partners/{partnerId}/network/siteIntent/{siteIntentId}")
def delete(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    site_intent_id: uuid.UUID = Query(alias="siteIntentId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.site_intent_cruds.get_by_site_intent_id(
        db=db, site_intent_id=site_intent_id
    )

    if not db_obj:
        err = f"Site intent {site_intent_id} not found"
        log.error(err)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": err},
        )

    if not db_obj.is_draft:
        log.info(f"Deleting the site intent {site_intent_id} over comcast")
        comcast_integration.SiteIntentIntegration(partner_id=partner_id).delete(
            site_intent_id=site_intent_id
        )

    cruds.site_intent_cruds.delete(db=db, db_obj=db_obj)

    log.info(f"Site intent {site_intent_id} deleted from db")

    return status.HTTP_204_NO_CONTENT


@router.put("/partners/{partnerId}/network/siteIntent/{siteIntentId}:push")
def push_to_comcast(
    partner_id: str = Path(alias="partnerId"),
    client_id: str = Query(None, alias="clientId"),
    site_intent_id: uuid.UUID = Query(alias="siteIntentId"),
    db: Session = Depends(get_db),
):
    db_obj = cruds.site_intent_cruds.get_by_site_intent_id(
        db=db, site_intent_id=site_intent_id
    )

    if not db_obj:
        err = f"Site intent {site_intent_id} not found"
        log.error(err)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": err},
        )

    if not db_obj.is_draft:
        err = f"Site intent id {site_intent_id} already pushed to comcast"
        log.error(err)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"message": err}
        )

    db_data = jsonable_encoder(db_obj.to_schema())
    comcast_input = {
        "siteIntentName": db_data.get("siteIntentName"),
        "refHubName": db_data.get("refHubName"),
        "refHubId": db_data.get("refHubId"),
        "csvIpOob": db_data.get("csvIpOob"),
    }

    comcast_response = comcast_integration.SiteIntentIntegration(
        partner_id=partner_id
    ).create(data=comcast_input)

    db_obj = cruds.site_intent_cruds.push(
        db=db, db_obj=db_obj, site_intent_id=comcast_response.get("siteIntentId")
    )

    log.info(f"Site intent {site_intent_id} record from comcast updated in db")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_obj.to_schema()),
    )
