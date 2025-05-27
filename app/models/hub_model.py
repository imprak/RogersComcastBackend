from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Boolean,
    String,
    UUID,
    func,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.models import Base
from app import schemas, models


class Hub(Base):
    __tablename__ = "hub"

    id = Column(Integer, primary_key=True, index=True)
    is_draft = Column(Boolean, default=True)
    hub_id = Column(UUID, unique=True)
    parent_hub_name = Column(String(255), nullable=False)
    ref_parent_hub_name = Column(String(255), nullable=False)
    ref_parent_hub_id = Column(UUID, nullable=False)
    hub_name = Column(String(255), nullable=False)
    hub_type = Column(String(255), nullable=False)
    ref_buhm_id = Column(UUID, nullable=False)
    ref_buhm_name = Column(String(255), nullable=False)
    postal_address = Column(Text(), nullable=True)
    timezone = Column(String(255), nullable=True)
    transaction_id = Column(
        UUID, ForeignKey("transaction.transaction_id"), nullable=True
    )
    order_id = Column(UUID, ForeignKey("order.order_id"), nullable=True)

    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())

    transaction = relationship("Transaction", back_populates="hubs")  # ORM relationship
    order = relationship("Order", back_populates="hubs")  # ORM relationship

    @classmethod
    def from_schema(
        cls,
        hub_id,
        schema: schemas.HubCreate,
        parent_hub_name: str,
        transaction_id: str | None = None,
        order_id: str | None = None,
    ) -> "Hub":
        content = {
            "hub_id": hub_id,
            "transaction_id": transaction_id,
            "order_id": order_id,
            "parent_hub_name": parent_hub_name,
            "ref_parent_hub_name": schema.ref_parent_hub_name,
            "ref_parent_hub_id": schema.ref_parent_hub_id,
            "hub_name": schema.hub_name,
            "hub_type": schema.hub_type,
            "ref_buhm_id": schema.ref_buhm_id,
            "ref_buhm_name": schema.ref_buhm_name,
            "postal_address": (
                "|".join(schema.postal_address.model_dump().values())
                if schema.postal_address
                else None
            ),
            "timezone": schema.timezone,
            "updated_by": schema.created_by,
            "created_by": schema.created_by,
        }

        return cls(**content)

    @staticmethod
    def from_update_schema(db_obj: "Hub", data_in: schemas.HubUpdate):
        db_obj.hub_name = data_in.hub_name
        db_obj.hub_type = data_in.hub_type
        db_obj.ref_buhm_id = data_in.ref_buhm_id
        db_obj.ref_buhm_name = data_in.ref_buhm_name
        db_obj.ref_parent_hub_name = data_in.ref_parent_hub_name
        db_obj.ref_parent_hub_id = data_in.ref_parent_hub_id
        db_obj.parent_hub_name = data_in.ref_parent_hub_name
        db_obj.timezone = data_in.timezone
        db_obj.created_by = data_in.created_by
        db_obj.updated_by = data_in.updated_by
        db_obj.postal_address = (
            "|".join(data_in.postal_address.model_dump().values())
            if data_in.postal_address
            else None
        )

        return db_obj

    def to_schema(self) -> schemas.HubReturn:
        content = {
            "hub_id": self.hub_id,
            "is_draft": self.is_draft,
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
            "transaction_id": self.transaction_id,
            "order_id": self.order_id,
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
