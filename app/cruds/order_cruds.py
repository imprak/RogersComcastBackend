from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import schemas, models
from app.core import enums


class OrderCrud:
    @staticmethod
    def create(db: Session, data_in: schemas.OrderCreate, order_id) -> models.Order:
        db_obj = models.Order.from_schema(schema=data_in, order_id=order_id)
        db.add(db_obj)
        db.commit()

        return db_obj

    @staticmethod
    def get_by_order_id(db: Session, order_id) -> models.Order:
        db_obj = (
            db.query(models.Order).filter(models.Order.order_id == order_id).first()
        )

        return db_obj

    @staticmethod
    def get_multi(db: Session, page=1, page_size=10) -> (list, int):
        offset = (page - 1) * page_size
        db_objs = (
            db.query(models.Order)
            .order_by(desc(models.Order.updated_by))
            .offset(offset)
            .limit(page_size)
            .all()
        )
        total_count = db.query(models.Order).count()

        return db_objs, total_count

    @staticmethod
    def get_multi_in_progress(db: Session, page=1, page_size=10):
        offset = (page - 1) * page_size
        db_objs = (
            db.query(models.Order)
            .filter(models.Order.order_status == enums.OrderStatus.IN_PROGRESS)
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return db_objs

    @staticmethod
    def delete(db: Session, db_obj: models.Order) -> None:
        db.delete(db_obj)
        db.commit()
