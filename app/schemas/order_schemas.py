from datetime import datetime

from pydantic import BaseModel, Field, UUID4, field_validator

from app.core import enums


class OrderBase(BaseModel):
    file_name: str = Field(alias="fileName")
    order_status: enums.OrderStatus = Field(alias="orderStatus")
    message: str | None = Field(None)
    api_name: enums.ApiNameEnums = Field(alias="apiName", examples=["hub"])

    created_by: str = Field(None, alias="createdBy", exclude=True)
    updated_by: str = Field(None, alias="updatedBy", exclude=True)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderReturn(OrderBase):
    order_id: UUID4 = Field(alias="orderId")
    hubs: int = Field(default=0)

    created_by: str | None = Field(None, alias="createdBy")
    updated_by: str | None = Field(None, alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    @field_validator("hubs", mode="before")
    def get_hub_count(cls, v: list):
        return len(v)
