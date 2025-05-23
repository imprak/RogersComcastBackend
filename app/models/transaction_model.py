import uuid
from sqlalchemy import Column, DateTime, Integer, String, func, Text, UUID, Enum
from sqlalchemy.orm import relationship

from app.core import enums
from app.models import Base
from app import schemas


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(UUID, nullable=False, unique=True)
    transaction_status = Column(Enum(enums.TransactionStatus), nullable=False)
    transaction_type = Column(Enum(enums.TransactionType), nullable=False)
    message = Column(Text(), nullable=True)

    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())

    hub = relationship("Hub", back_populates="transaction")
    order = relationship("Order", back_populates="transaction")

    @classmethod
    def from_schema(
        cls, schema: schemas.TransactionCreate, transaction_id
    ) -> "Transaction":
        return cls(
            **{
                "transaction_id": transaction_id,
                "transaction_status": schema.transaction_status,
                "transaction_type": schema.transaction_type,
                "message": schema.message,
                "created_by": schema.created_by,
                "updated_by": schema.created_by,
            }
        )

    def to_schema(self) -> schemas.TransactionReturn:
        return schemas.TransactionReturn.model_validate(
            self, by_name=True, from_attributes=True
        ).model_dump(by_alias=True)
