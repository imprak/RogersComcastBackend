from sqlalchemy.orm import Session

from app import schemas, models


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
    def get_multi(db: Session, page=1, page_size=10) -> list:
        offset = (page - 1) * page_size
        db_objs = db.query(models.Order).offset(offset).limit(page_size).all()

        return db_objs

    @staticmethod
    def delete(db: Session, db_obj: models.Order) -> None:
        db.delete(db_obj)
        db.commit()
