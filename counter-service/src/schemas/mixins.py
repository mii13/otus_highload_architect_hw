from datetime import datetime

from pydantic import BaseModel


class TimestampSchemaMixin(BaseModel):
    # BaseModel - если не наследоваться, то поля не добавляются
    created_at: datetime
    updated_at: datetime
