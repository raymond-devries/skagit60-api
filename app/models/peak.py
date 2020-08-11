import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, HttpUrl, confloat, conint, constr


class Peak(BaseModel):
    name: constr(max_length=100)
    display_name: constr(max_length=100)
    elevation: conint(ge=0, lt=30000)
    lat: confloat(ge=-90, le=90)
    long: confloat(ge=-180, le=180)
    peakbagger_link = HttpUrl


class Tick(BaseModel):
    climber: str
    date: datetime.date


class InterestedClimber(BaseModel):
    climber: str
