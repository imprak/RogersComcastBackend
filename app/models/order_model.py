from sqlalchemy import Column, DateTime, String, Integer, func, UUID, Enum
from sqlalchemy.orm import relationship

from app.models import Base
from app import schemas
from app.core import enums


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(UUID, nullable=False, unique=True)
    api_name = Column(Enum(enums.ApiNameEnums), nullable=False)
    file_name = Column(String(255), nullable=False)
    order_status = Column(Enum(enums.TransactionStatus), nullable=False)
    message = Column(String(255), nullable=True)
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())

    hubs = relationship("Hub", back_populates="order")
    site_intents = relationship("SiteIntent", back_populates="order")
    ppod_intents = relationship("PpodIntent", back_populates="order")

    @classmethod
    def from_schema(cls, schema: schemas.OrderCreate, order_id) -> "Order":
        return cls(
            **{
                "order_id": order_id,
                "api_name": schema.api_name,
                "file_name": schema.file_name,
                "order_status": schema.order_status,
                "message": schema.message,
                "created_by": schema.created_by,
                "updated_by": schema.created_by,
            }
        )

    def to_schema(self) -> schemas.OrderReturn:
        return schemas.OrderReturn.model_validate(
            self, by_name=True, from_attributes=True
        ).model_dump(by_alias=True)
