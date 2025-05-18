from uuid import UUID as CORE_UUID
from sqlalchemy import Column, DateTime, String, func, UUID

from app.models.base import Base
from app import schemas


class Order(Base):
    __tablename__ = "order"
    order_id = Column(UUID, nullable=False)
    created_by = Column(String(255), nullable=False)
    updated_by = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())

    @classmethod
    def from_schema(cls, schema: schemas.OrderCreate, order_id: CORE_UUID) -> "Order":
        return cls(
            **{
                "order_id": order_id,
                "created_by": schema.created_by,
                "updated_by": schema.created_by,
            }
        )

    def to_schema(self) -> schemas.OrderReturn:
        return schemas.OrderReturn.model_validate(
            self, by_name=True, from_attributes=True
        ).model_dump(by_alias=True)
