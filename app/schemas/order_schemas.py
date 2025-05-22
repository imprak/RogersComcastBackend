from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, UUID4

from app.core import enums


class OrderBase(BaseModel):
    file_name: str = Field(alias="fileName")
    transaction_id: UUID4 = Field(alias="transactionId")
    order_status: enums.OrderStatus = Field(alias="orderStatus")
    message: str | None = Field(None)

    created_by: str = Field(None, alias="createdBy", exclude=True)
    updated_by: str = Field(None, alias="updatedBy", exclude=True)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderReturn(OrderBase):
    order_id: UUID4 = Field(alias="orderId")

    created_by: str | None = Field(None, alias="createdBy")
    updated_by: str | None = Field(None, alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
