from sqlalchemy.orm import Session

from app import schemas, models


class ApiCrud:
    @staticmethod
    def create(db: Session, data_in: schemas.ApiCreate, api_id) -> models.Api:
        db_obj = models.Api.from_schema(schema=data_in, api_id=api_id)
        db.add(db_obj)
        db.commit()

        return db_obj

    @staticmethod
    def get_by_api_id(db: Session, api_id) -> models.Api:
        db_obj = db.query(models.Api).filter(models.Api.api_id == api_id).first()

        return db_obj

    @staticmethod
    def get_multi(db: Session, page=1, page_size=10) -> list:
        offset = (page - 1) * page_size
        db_objs = db.query(models.Api).offset(offset).limit(page_size).all()

        return db_objs

    @staticmethod
    def delete(db: Session, db_obj: models.Api) -> None:
        db.delete(db_obj)
        db.commit()
