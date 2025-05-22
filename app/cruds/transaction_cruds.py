from sqlalchemy.orm import Session

from app import schemas, models


class TransactionCrud:
    @staticmethod
    def create(
        db: Session, data_in: schemas.TransactionCreate, transaction_id
    ) -> models.Transaction:
        db_obj = models.Transaction.from_schema(
            schema=data_in, transaction_id=transaction_id
        )
        db.add(db_obj)
        db.commit()

        return db_obj

    @staticmethod
    def get_by_transaction_id(db: Session, transaction_id) -> models.Transaction:
        db_obj = (
            db.query(models.Transaction)
            .filter(models.Transaction.transaction_id == transaction_id)
            .first()
        )

        return db_obj

    @staticmethod
    def get_multi(db: Session, page=1, page_size=10) -> list:
        offset = (page - 1) * page_size
        db_objs = db.query(models.Transaction).offset(offset).limit(page_size).all()

        return db_objs

    @staticmethod
    def delete(db: Session, db_obj: models.Transaction) -> None:
        db.delete(db_obj)
        db.commit()
