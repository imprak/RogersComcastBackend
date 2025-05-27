from datetime import datetime

from pydantic import BaseModel, Field, UUID4

from app.core import enums


class ApiBase(BaseModel):
    api_name: enums.ApiNameEnums = Field(alias="apiName", examples=["hub"])
    api_category: str = Field(alias="apiCategory")
    comment: str

    created_by: str = Field(None, alias="createdBy", exclude=True)
    updated_by: str = Field(None, alias="updatedBy", exclude=True)


class ApiCreate(ApiBase):
    pass


class ApiUpdate(ApiBase):
    pass


class ApiReturn(ApiBase):
    api_id: UUID4 = Field(alias="apiId")
    created_by: str | None = Field(None, alias="createdBy")
    updated_by: str | None = Field(None, alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
