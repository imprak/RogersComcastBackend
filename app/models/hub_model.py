from uuid import UUID as CORE_UUID

from sqlalchemy import Column, DateTime, Integer, String, UUID, func, Text

from app.models.base import Base
from app import schemas


class Hub(Base):
    __tablename__ = "hub"

    id = Column(Integer, primary_key=True, index=True)
    hub_id = Column(UUID, nullable=False)
    parent_hub_name = Column(String(255), nullable=False)
    ref_parent_hub_name = Column(String(255), nullable=False)
    ref_parent_hub_id = Column(UUID, nullable=False)
    hub_name = Column(String(255), nullable=False)
    hub_type = Column(String(255), nullable=False)
    ref_buhm_id = Column(UUID, nullable=False)
    ref_buhm_name = Column(String(255), nullable=False)
    postal_address = Column(Text(), nullable=False)
    timezone = Column(String(255), nullable=False)

    created_by = Column(String(255), nullable=False)
    updated_by = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())

    @classmethod
    def from_schema(
        cls, schema: schemas.HubCreate, hub_id: CORE_UUID, parent_hub_name: str
    ) -> "Hub":
        content = {
            "hub_id": hub_id,
            "parent_hub_name": parent_hub_name,
            "ref_parent_hub_name": schema.ref_parent_hub_name,
            "ref_parent_hub_id": schema.ref_parent_hub_id,
            "hub_name": schema.hub_name,
            "hub_type": schema.hub_type,
            "ref_buhm_id": schema.ref_buhm_id,
            "ref_buhm_name": schema.ref_buhm_name,
            "postal_address": "|".join(schema.postal_address.model_dump().values()),
            "timezone": schema.timezone,
            "updated_by": schema.created_by,
            "created_by": schema.created_by,
        }

        return cls(**content)

    def to_schema(self) -> schemas.HubReturn:
        content = {
            "hub_id": self.hub_id,
            "parent_hub_name": self.parent_hub_name,
            "hub_name": self.hub_name,
            "hub_type": self.hub_type,
            "ref_buhm_id": self.ref_buhm_id,
            "ref_buhm_name": self.ref_buhm_name,
            "timezone": self.timezone,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if self.postal_address:
            content.update(
                {
                    "postal_address": {
                        "addr1": self.postal_address.split("|")[0],
                        "addr2": self.postal_address.split("|")[1],
                        "administrative_area": self.postal_address.split("|")[2],
                        "country": self.postal_address.split("|")[3],
                        "postal_code": self.postal_address.split("|")[4],
                    },
                }
            )

        return schemas.HubReturn.model_validate(content, by_name=True).model_dump(
            by_alias=True
        )
