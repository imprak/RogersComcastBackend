from sqlalchemy.orm import Session

from app import schemas, models


class PpodIntentCrud:
    @staticmethod
    def create(db: Session, data_in: schemas.PpodIntentCreate) -> models.PpodIntent:
        db_obj = models.PpodIntent.from_schema(schema=data_in)
        db.add(db_obj)
        db.commit()

        return db_obj

    @staticmethod
    def get_by_ppod_intent_id(db: Session, ppod_intent_id) -> models.PpodIntent:
        db_obj = (
            db.query(models.PpodIntent)
            .filter(models.PpodIntent.ppod_intent_id == ppod_intent_id)
            .first()
        )

        return db_obj

    @staticmethod
    def get_multi(db: Session, page=1, page_size=10) -> list:
        offset = (page - 1) * page_size
        db_objs = db.query(models.PpodIntent).offset(offset).limit(page_size).all()

        return db_objs

    @staticmethod
    def delete(db: Session, db_obj: models.PpodIntent) -> None:
        db.delete(db_obj)
        db.commit()

    @staticmethod
    def push(
        db: Session, db_obj: models.PpodIntent, ppod_intent_id, cpod_intent_id=None
    ) -> models.PpodIntent:
        db_obj.ppod_intent_id = ppod_intent_id
        db_obj.cpod_intent_id = cpod_intent_id
        db_obj.is_draft = False
        db.commit()

        return db_obj
