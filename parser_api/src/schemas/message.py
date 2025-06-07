from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)

from schemas.enums import (
    EXAMPLE_FULL_REQUEST,
    SchemaDescription,
    SchemaExample,
    SchemaTitle,
)
from services.enums import StatusType


class AccountData(BaseModel):
    account: str = Field(
        ...,
        title=SchemaTitle.ACCOUNT.value,
        description=SchemaDescription.ACCOUNT.value,
        example=SchemaExample.ACCOUNT.value,
    )
    city: Optional[str] = Field(
        None,
        title=SchemaTitle.CITY.value,
        description=SchemaDescription.CITY.value,
        example=SchemaExample.CITY.value,
    )
    account_type: str = Field(
        ...,
        title=SchemaTitle.ACCOUNT_TYPE.value,
        description=SchemaDescription.ACCOUNT_TYPE.value,
        example=SchemaExample.ACCOUNT_TYPE.value)
    utility: str = Field(
        ...,
        title=SchemaTitle.UTILITY.value,
        description=SchemaDescription.UTILITY.value,
        example=SchemaExample.UTILITY.value,
    )
    status_response: Optional[StatusType] = Field(
        None,
        title=SchemaTitle.STATUS_RESPONSE.value,
        description=SchemaDescription.STATUS_RESPONSE.value,
        example=SchemaExample.STATUS_RESPONSE.value,
    )
    response: Optional[dict] = Field(
        None,
        title=SchemaTitle.RESPONSE.value,
        description=SchemaDescription.RESPONSE.value,
        example=SchemaExample.RESPONSE.value,
    )


class BaseMessageData(BaseModel):
    tg_id: str = Field(
        ...,
        title=SchemaTitle.TG_ID.value,
        description=SchemaDescription.TG_ID.value,
        example=SchemaExample.TG_ID.value,
    )
    job_status: StatusType = Field(
        ...,
        title=SchemaTitle.JOB_STATUS.value,
        description=SchemaDescription.JOB_STATUS.value,
        example=SchemaExample.JOB_STATUS.value,
    )
    data: list[AccountData] = Field(
        ...,
        title=SchemaTitle.DATA.value,
        description=SchemaDescription.DATA.value,
    )
    notify: str = Field(
        ...,
        title=SchemaTitle.NOTIFY.value,
        description=SchemaDescription.NOTIFY.value,
        example=SchemaExample.NOTIFY.value,
    )
    first_check: str = Field(
        ...,
        title=SchemaTitle.FIRST_CHECK.value,
        description=SchemaDescription.FIRST_CHECK.value,
        example=SchemaExample.FIRST_CHECK.value,
    )

    class Config:
        extra = 'forbid'
        json_schema_extra = EXAMPLE_FULL_REQUEST


class ResultOutPutMessageData(BaseMessageData):
    """Схема возврата результата парсинга."""
