import uuid

from sqlalchemy import Column, DateTime, String, Integer, func, UUID, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base
from app import schemas
from app.core import enums


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(UUID, nullable=False, unique=True)
    file_name = Column(String(255), nullable=False)
    order_status = Column(Enum(enums.TransactionStatus), nullable=False)
    message = Column(String(255), nullable=True)
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    transaction_id = Column(
        UUID, ForeignKey("transaction.transaction_id"), nullable=False
    )

    transaction = relationship(
        "Transaction", back_populates="order"
    )  # ORM relationship
    hubs = relationship("Hub", back_populates="order")

    @classmethod
    def from_schema(cls, schema: schemas.OrderCreate, order_id) -> "Order":
        return cls(
            **{
                "order_id": order_id,
                "file_name": schema.file_name,
                "order_status": schema.order_status,
                "message": schema.message,
                "transaction_id": schema.transaction_id,
                "created_by": schema.created_by,
                "updated_by": schema.created_by,
            }
        )

    def to_schema(self) -> schemas.OrderReturn:
        return schemas.OrderReturn.model_validate(
            self, by_name=True, from_attributes=True
        ).model_dump(by_alias=True)
