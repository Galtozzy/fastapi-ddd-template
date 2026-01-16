from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


def decimal_serializer(value: Decimal | int | float | None) -> float | None:
    if value is None:
        return None

    if isinstance(value, float | int):
        return value

    return float(value.quantize(Decimal('0.0000'), rounding=ROUND_HALF_UP))


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={Decimal: decimal_serializer},
        from_attributes=True,
    )
