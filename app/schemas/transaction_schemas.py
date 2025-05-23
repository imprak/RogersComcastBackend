from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, UUID4, model_validator

from app.core import enums


class TransactionBase(BaseModel):
    transaction_status: enums.TransactionStatus = Field(alias="transactionStatus")
    transaction_type: enums.TransactionType = Field(alias="transactionType")
    message: Optional[str] = Field(None)
    created_by: str = Field(None, alias="createdBy", exclude=True)
    updated_by: str = Field(None, alias="updatedBy", exclude=True)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionReturn(TransactionBase):
    transaction_id: UUID4 = Field(alias="transactionId")

    created_by: str | None = Field(None, alias="createdBy")
    updated_by: str | None = Field(None, alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
