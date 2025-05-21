from sqlalchemy.orm import Session

from app import schemas, models


class SiteIntentCrud:
    @staticmethod
    def create(db: Session, data_in: schemas.SiteIntentCreate) -> models.SiteIntent:
        db_obj = models.SiteIntent.from_schema(schema=data_in)
        db.add(db_obj)
        db.commit()

        return db_obj

    @staticmethod
    def get_by_site_intent_id(db: Session, site_intent_id) -> models.SiteIntent:
        db_obj = (
            db.query(models.SiteIntent)
            .filter(models.SiteIntent.site_intent_id == site_intent_id)
            .first()
        )

        return db_obj

    @staticmethod
    def get_multi(db: Session, page=1, page_size=10) -> list:
        offset = (page - 1) * page_size
        db_objs = db.query(models.SiteIntent).offset(offset).limit(page_size).all()

        return db_objs

    @staticmethod
    def delete(db: Session, db_obj: models.SiteIntent) -> None:
        db.delete(db_obj)
        db.commit()

    @staticmethod
    def push(
        db: Session, db_obj: models.SiteIntent, site_intent_id
    ) -> models.SiteIntent:
        db_obj.site_intent_id = site_intent_id
        db_obj.is_draft = False
        db.commit()

        return db_obj
