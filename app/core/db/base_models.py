import uuid
from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from pydantic import ConfigDict
from sqlmodel import DateTime, SQLModel, func
from sqlmodel.main import Field

from app.core.pydantic_base import decimal_serializer


class BaseSQLModel(SQLModel):
    model_config = ConfigDict(json_encoders={Decimal: decimal_serializer})  # type: ignore[assignment]


class DBBaseModel(BaseSQLModel):
    __tablename__: ClassVar[str | Callable[..., str]]  # pyright: ignore[reportIncompatibleVariableOverride]
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    created_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore[call-overload]
        sa_column_kwargs={'server_default': func.now()},
        nullable=False,
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore[call-overload]
        sa_column_kwargs={'onupdate': func.now(), 'server_default': func.now()},
        nullable=False,
    )
