from datetime import datetime
from typing import List, Optional

from pydantic import Field, UUID4, BaseModel


class Ip(BaseModel):
    ipv4: List[str]
    ipv6: List[str]


class IpAllocation(BaseModel):
    comcast_routable: Ip = Field(alias="comcastRoutable")
    partner_internal: Ip = Field(alias="partnerInternal")
    internet_routed: Ip = Field(alias="internetRouted")


class SiteIntentBase(BaseModel):
    site_intent_name: str = Field(alias="siteIntentName")
    ref_hub_name: str = Field(alias="refHubName")
    ref_hub_id: UUID4 = Field(
        examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="refHubId"
    )
    csv_ip_oob: Optional[str] = Field(None, alias="csvIpOob")
    ip_allocation: Optional[IpAllocation] = Field(None, alias="ipAllocation")

    created_by: str = Field(None, alias="createdBy", exclude=True)
    updated_by: str = Field(None, alias="updatedBy", exclude=True)


class SiteIntentCreate(SiteIntentBase):
    pass


class SiteIntentUpdate(SiteIntentBase):
    pass


class SiteIntentReturn(SiteIntentBase):
    site_intent_id: Optional[UUID4] = Field(
        None, examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="siteIntentId"
    )
    is_draft: bool = Field(True, alias="isDraft")

    created_by: str = Field(alias="createdBy")
    updated_by: str = Field(alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    transaction_id: Optional[UUID4] = Field(alias="transactionId")
    order_id: Optional[UUID4] = Field(None, alias="orderId")
