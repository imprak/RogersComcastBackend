from datetime import datetime

from pydantic import BaseModel, Field, UUID4


class ApiBase(BaseModel):
    api_name: str = Field(alias="apiName")
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
    created_by: str = Field(alias="createdBy")
    updated_by: str = Field(alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
