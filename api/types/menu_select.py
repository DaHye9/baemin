from datetime import datetime
from typing import Literal

import pydantic

from api.types.common import statusT

ErrorT = Literal['INSUFFICIENT_INGREDIENTS', 'INVALID REQUEST', 'MENU_NOT_FOUND']
class MenuSelectInfo(pydantic.BaseModel):
    menuId: str
    quantity: int
    shopId: str
    memberNo: str

class MenuSelectData(pydantic.BaseModel):
    reservationId: str
    reservationExpiresAt: datetime
    menuId: str
    quantity: int

class MenuSelectResponse(pydantic.BaseModel):
    status: statusT
    message: str
    timestamp: datetime
    data: MenuSelectData | None
    error_code: ErrorT | None

    @pydantic.field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, value: str) -> datetime:
        return datetime.fromisoformat(value)

    @pydantic.model_validator(mode='after')
    @classmethod
    def check_error_code(cls, model: 'MenuSelectResponse') -> 'MenuSelectResponse':
        if model.status == 'ERROR' and not model.error_code:
            raise ValueError('error_code must be provided when status is ERROR')
        return model
