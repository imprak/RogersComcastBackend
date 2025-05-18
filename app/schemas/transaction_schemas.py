from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, UUID4

from app.core import enums


class TransactionBase(BaseModel):
    transaction_status: enums.TransactionStatus = Field(alias="transactionStatus")
    transaction_type: enums.TransactionType = Field(alias="transactionType")
    message: Optional[str]
    created_by: str = Field(None, alias="createdBy", exclude=True)
    updated_by: str = Field(None, alias="updatedBy", exclude=True)


class TransactionCreate(BaseModel):
    pass


class TransactionUpdate(BaseModel):
    pass


class TransactionReturn(BaseModel):
    transaction_id: UUID4 = Field(alias="transactionId")

    created_by: str = Field(alias="createdBy")
    updated_by: str = Field(alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
