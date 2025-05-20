from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4, Field


class PostalAddress(BaseModel):
    addr1: str
    addr2: str
    administrative_area: str = Field(alias="administrativeArea")
    country: str
    postal_code: str = Field(alias="postalCode")


class HubBase(BaseModel):
    hub_name: str = Field(alias="hubName")
    hub_type: str = Field(alias="hubType")
    ref_buhm_id: UUID4 = Field(
        examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="refBuhmId"
    )
    ref_buhm_name: str = Field(alias="refBuhmName")
    postal_address: Optional[PostalAddress] = Field(None, alias="postalAddress")
    timezone: Optional[str] = Field(None)

    created_by: str = Field(None, alias="createdBy", exclude=True)
    updated_by: str = Field(None, alias="updatedBy", exclude=True)


class HubCreate(HubBase):
    ref_parent_hub_name: str = Field(alias="refParentHubName")
    ref_parent_hub_id: UUID4 = Field(
        examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="refParentHubId"
    )


class HubUpdate(HubBase):
    ref_parent_hub_name: str = Field(alias="refParentHubName")
    ref_parent_hub_id: UUID4 = Field(
        examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="refParentHubId"
    )


class HubReturn(HubBase):
    hub_id: Optional[UUID4] = Field(
        None, examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="hubId"
    )
    parent_hub_name: str = Field(alias="parentHubName")
    is_draft: bool = Field(True, alias="isDraft")
    created_by: str = Field(alias="createdBy")
    updated_by: str = Field(alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
