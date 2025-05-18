from uuid import UUID as CORE_UUID

from sqlalchemy import Column, DateTime, Integer, String, UUID, func, Text

from app.models.base import Base
from app import schemas


class SiteIntent(Base):
    __tablename__ = "site_intent"

    id = Column(Integer, primary_key=True, index=True)
    site_intent_id = Column(UUID, nullable=False)
    site_intent_name = Column(String(255), nullable=False)
    ref_hub_name = Column(String(255), nullable=False)
    ref_hub_id = Column(UUID, nullable=False)
    csv_ip_oob = Column(String(255), nullable=True)

    comcast_routable_ipv4 = Column(Text(), nullable=True)
    comcast_routable_ipv6 = Column(Text(), nullable=True)
    partner_internal_ipv4 = Column(Text(), nullable=True)
    partner_internal_ipv6 = Column(Text(), nullable=True)
    internet_routed_ipv4 = Column(Text(), nullable=True)
    internet_routed_ipv6 = Column(Text(), nullable=True)

    created_by = Column(String(255), nullable=False)
    updated_by = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())

    @classmethod
    def from_schema(
        cls, schema: schemas.SiteIntentCreate, site_intent_id: CORE_UUID
    ) -> "SiteIntent":
        content = {
            "site_intent_id": site_intent_id,
            "site_intent_name": schema.site_intent_name,
            "ref_hub_name": schema.ref_hub_name,
            "ref_hub_id": schema.ref_hub_id,
            "csv_ip_oob": schema.csv_ip_oob,
            "updated_by": schema.created_by,
            "created_by": schema.created_by,
        }

        if schema.ip_allocation:
            content.update(
                {
                    "comcast_routable_ipv4": ", ".join(
                        schema.ip_allocation.comcast_routable.ipv4
                    ),
                    "comcast_routable_ipv6": ", ".join(
                        schema.ip_allocation.comcast_routable.ipv6
                    ),
                    "partner_internal_ipv4": ", ".join(
                        schema.ip_allocation.partner_internal.ipv4
                    ),
                    "partner_internal_ipv6": ", ".join(
                        schema.ip_allocation.partner_internal.ipv6
                    ),
                    "internet_routed_ipv4": ", ".join(
                        schema.ip_allocation.internet_routed.ipv4
                    ),
                    "internet_routed_ipv6": ", ".join(
                        schema.ip_allocation.internet_routed.ipv6
                    ),
                }
            )

        return cls(**content)

    def to_schema(self) -> schemas.SiteIntentReturn:
        content = {
            "site_intent_id": self.site_intent_id,
            "site_intent_name": self.site_intent_name,
            "ref_hub_name": self.ref_hub_name,
            "ref_hub_id": self.ref_hub_id,
            "csv_ip_oob": self.csv_ip_oob,
            "ip_allocation": {
                "comcast_routable": {
                    "ipv4": self.comcast_routable_ipv4.split(", "),
                    "ipv6": self.comcast_routable_ipv6.split(", "),
                },
                "partner_internal": {
                    "ipv4": self.partner_internal_ipv4.split(", "),
                    "ipv6": self.partner_internal_ipv6.split(", "),
                },
                "internet_routed": {
                    "ipv4": self.partner_internal_ipv4.split(", "),
                    "ipv6": self.partner_internal_ipv6.split(", "),
                },
            },
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return schemas.SiteIntentReturn.model_validate(
            content, by_name=True
        ).model_dump(by_alias=True)
