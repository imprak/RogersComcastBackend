from uuid import UUID as CORE_UUID
from sqlalchemy import Column, DateTime, Integer, String, func, Text, UUID, Enum

from app.core import enums
from app.models.base import Base
from app import schemas


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(UUID, nullable=False)
    transaction_status = Column(Enum(enums.TransactionStatus), nullable=False)
    transaction_type = Column(Enum(enums.TransactionType), nullable=False)
    message = Column(Text(), nullable=True)

    created_by = Column(String(255), nullable=False)
    updated_by = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())

    @classmethod
    def from_schema(
        cls, schema: schemas.TransactionCreate, transaction_id: CORE_UUID
    ) -> "Transaction":
        return cls(
            **{
                "transaction_id": transaction_id,
                "transaction_status": schema.transaction_status,
                "transaction_type": schema.transaction_type,
                "message": schema.message,
                "created_by": schema.created_by,
                "created_at": schema.created_by,
            }
        )

    def to_schema(self) -> schemas.TransactionReturn:
        return schemas.TransactionReturn.model_validate(
            self, by_name=True, from_attributes=True
        ).model_dump(by_alias=True)
