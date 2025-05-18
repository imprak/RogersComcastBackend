from datetime import datetime

from pydantic import BaseModel, Field, UUID4


class OrderBase(BaseModel):
    created_by: str = Field(None, alias="createdBy", exclude=True)
    updated_by: str = Field(None, alias="updatedBy", exclude=True)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderReturn(OrderBase):
    order_id: UUID4 = Field(alias="orderId")

    created_by: str = Field(alias="createdBy")
    updated_by: str = Field(alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
