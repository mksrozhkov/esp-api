# stdlib
from datetime import datetime

# thirdparty
from pydantic import BaseModel


class MeasurementInputSchema(BaseModel):
    temp: int
    humidity: int
    pressure: int


class MeasurementOutputSchema(MeasurementInputSchema):
    created_at: datetime


class MeasurementListFilterSchema(BaseModel):
    time_from: datetime
    time_to: datetime
