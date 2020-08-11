from typing import Optional
from pydantic import BaseModel, constr, conint, confloat, HttpUrl
from bson import ObjectId
import datetime


class Peak(BaseModel):
    name: constr(max_length=100)
    display_name: constr(max_length=100)
    elevation: conint(ge=0, lt=30000)
    lat: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)
    peakbagger_link = HttpUrl


class Tick(BaseModel):
    climber: ObjectId
    date: datetime.date


class InterestedClimber(BaseModel):
    climber: ObjectId
