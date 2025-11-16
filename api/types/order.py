from datetime import datetime
from typing import Literal

import pydantic

from api.types.common import statusT

dataStatusT = Literal['INITIALIZING']
ErrorT = Literal['RESERVATION_EXPIRED', 'INGREDIENTS_EXHAUSTED', 'INVALID_RESERVATION']

class OrderRequest(pydantic.BaseModel):
    reservationId: str
    memberNo: str

class MemberInfo(pydantic.BaseModel):
    memberNo: str

class OrderData(pydantic.BaseModel):
    orderNo: str
    orderStatus: dataStatusT
    reservationId: str
    createdAt: datetime
    memberInfo: MemberInfo

    @pydantic.field_validator('createdAt', mode='before')
    @classmethod
    def parse_created_at(cls, value: str) -> datetime:
        return datetime.fromisoformat(value)


class OrderResponse(pydantic.BaseModel):
    status: statusT
    message: str
    timestamp: datetime
    data: OrderData | None
    error_code: ErrorT | None

    @pydantic.field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, value: str) -> datetime:
        return datetime.fromisoformat(value)

    @pydantic.model_validator(mode='after')
    @classmethod
    def check_error_code(cls, model: 'OrderResponse') -> 'OrderResponse':
        if model.status == 'ERROR' and not model.error_code:
            raise ValueError('error_code must be provided when status is ERROR')
        return model
