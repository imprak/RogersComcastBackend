from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import schemas, models


class HubCrud:
    @staticmethod
    def create(
        db: Session,
        hub_id,
        data_in: schemas.HubCreate,
        parent_hub_name,
        transaction_id=None,
        order_id=None,
    ) -> models.Hub:
        db_obj = models.Hub.from_schema(
            schema=data_in,
            parent_hub_name=parent_hub_name,
            transaction_id=transaction_id,
            hub_id=hub_id,
            order_id=order_id,
        )
        db.add(db_obj)
        db.commit()

        return db_obj

    @staticmethod
    def update(
        db: Session,
        db_obj: models.Hub,
        data_in: schemas.HubUpdate,
    ) -> models.Hub:
        db_obj = models.Hub.from_update_schema(db_obj=db_obj, data_in=data_in)
        db.commit()

        return db_obj

    @staticmethod
    def get_by_hub_id(db: Session, hub_id) -> models.Hub:
        db_obj = db.query(models.Hub).filter(models.Hub.hub_id == hub_id).first()

        return db_obj

    @staticmethod
    def get_by_draft_id(db: Session, draft_id) -> models.Hub:
        db_obj = db.query(models.Hub).filter(models.Hub.id == draft_id).first()

        return db_obj

    @staticmethod
    def get_multi(db: Session, page=1, page_size=10) -> (list, int):
        offset = (page - 1) * page_size
        db_objs = (
            db.query(models.Hub)
            .order_by(desc(models.Hub.updated_at))
            .offset(offset)
            .limit(page_size)
            .all()
        )
        total_count = db.query(models.Hub).count()

        return db_objs, total_count

    @staticmethod
    def delete(db: Session, db_obj: models.Hub) -> None:
        db.delete(db_obj)
        db.commit()

    @staticmethod
    def push(db: Session, db_obj: models.Hub, hub_id, transaction_id) -> models.Hub:
        db_obj.hub_id = hub_id
        db_obj.transaction_id = transaction_id
        db_obj.is_draft = False
        db.commit()

        return db_obj
