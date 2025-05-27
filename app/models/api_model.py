from uuid import UUID as CORE_UUID
from sqlalchemy import Column, DateTime, Integer, String, func, Text, UUID, Enum

from app.models import Base
from app import schemas
from app.core import enums


class Api(Base):
    __tablename__ = "api"

    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(UUID, nullable=False)
    api_name = Column(Enum(enums.ApiNameEnums), unique=True, nullable=False)
    api_category = Column(String(255), nullable=False)
    comment = Column(Text(), nullable=True)

    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())

    @classmethod
    def from_schema(cls, schema: schemas.ApiCreate, api_id: CORE_UUID) -> "Api":
        return cls(
            **{
                "api_id": api_id,
                "api_name": schema.api_name,
                "api_category": schema.api_category,
                "comment": schema.comment,
                "created_by": schema.created_by,
                "updated_by": schema.updated_by,
            }
        )

    def to_schema(self) -> schemas.ApiCreate:
        return schemas.ApiReturn.model_validate(
            self, by_name=True, from_attributes=True
        ).model_dump(by_alias=True)
