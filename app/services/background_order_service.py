import time
import uuid

from sqlalchemy.orm import Session
import pandas as pd

from app.core.config import settings
from app.core import enums
from app.dependencies.db_session import get_db
from app import models, cruds, schemas, log


class OrderValidation:
    def __init__(self, db: Session):
        self.db = db
        self.db_obj_orders = cruds.order_cruds.get_multi_in_progress(self.db)

    def validate_orders(self, db_obj_order: models.Order):
        log.info(f"Validating order {db_obj_order.order_id}")
        full_file_path = f"{settings.ORDER_STORAGE_PATH}/{db_obj_order.file_name}"
        df = pd.read_csv(full_file_path)
        record_list = df.to_dict(orient="records")
        log.info(f"record_list count {len (record_list)}")
        success_record_list = []
        errored_record_list = []

        for record in record_list:
            try:
                data_in = schemas.HubCreate.model_validate(record)
                hub_id = uuid.uuid4()
                cruds.hub_cruds.create(
                    db=self.db,
                    data_in=data_in,
                    parent_hub_name=data_in.ref_parent_hub_name,
                    hub_id=hub_id,
                    transaction_id=db_obj_order.transaction_id,
                    order_id=db_obj_order.order_id,
                )
                success_record_list.append(record)
            except Exception as err:
                log.error(
                    f"Validation error for order {db_obj_order.order_id}, record {str(record)}. Error- {err}"
                )
                errored_record_list.append(record)

        if errored_record_list:
            db_obj_order.order_status = enums.OrderStatus.FAILED
            db_obj_order.message = "failed"
            self.db.commit()
            df = pd.DataFrame(errored_record_list)
            df.to_csv(full_file_path, index=False)

        if success_record_list:
            db_obj_transaction = cruds.transaction_cruds.get_by_transaction_id(
                db=self.db, transaction_id=db_obj_order.transaction_id
            )
            db_obj_transaction.transaction_status = enums.TransactionStatus.COMPLETED
            db_obj_transaction.message = "completed"
            if not errored_record_list:
                db_obj_order.order_status = enums.OrderStatus.COMPLETED
                db_obj_order.message = "completed"
            self.db.commit()

        else:
            db_obj_transaction = cruds.transaction_cruds.get_by_transaction_id(
                db=self.db, transaction_id=db_obj_order.transaction_id
            )
            db_obj_transaction.transaction_status = enums.TransactionStatus.FAILED
            db_obj_transaction.message = "failed"
            self.db.commit()


def trigger_order_validation():
    log.info("Order validation service started in background")
    while True:
        db = None
        try:
            db = next(get_db())
            order_validation = OrderValidation(db=db)
            log.info(
                f"Fetched {len(order_validation.db_obj_orders)} orders to validate"
            )
            for db_obj_order in order_validation.db_obj_orders:
                try:
                    order_validation.validate_orders(db_obj_order)
                except Exception as err:
                    log.error(
                        f"Error occurred while validating the order {str(db_obj_order.order_id)}: {str(err)}"
                    )
                    continue
        except Exception as err:
            log.error(f"Error occurred while validating the orders: {str(err)}")
        finally:
            if db:
                db.close()

        time.sleep(5)
