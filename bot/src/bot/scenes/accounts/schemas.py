import re

from pydantic import BaseModel, field_validator


class AccountInput(BaseModel):
    value: str

    @field_validator('value')
    def must_be_non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Ошибка: передано пустое значение!')
        return v

    @field_validator('value')
    def must_be_numeric_and_valid_length(cls, v: str) -> str:
        cleaned = re.sub(r'[-()+]', '', v)
        if not cleaned.isdigit():
            raise ValueError(
                'Ошибка: значение не является числом!'
            )
        if len(cleaned) < 3:
            raise ValueError(
                'Ошибка: неполный номер лицевого счета или телефона!'
            )
        return cleaned
