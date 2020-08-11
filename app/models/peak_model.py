import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, confloat, conint, constr, validator
from slugify import slugify


class Peak(BaseModel):
    name: constr(max_length=100)
    display_name: constr(max_length=100)
    elevation: conint(ge=0, lt=30000)
    lat: confloat(ge=-90, le=90)
    long: confloat(ge=-180, le=180)
    state: constr(max_length=50)
    country: constr(max_length=3)
    peakbagger_link: HttpUrl
    slug: Optional[str] = None

    @validator("slug", pre=True, always=True)
    def create_slug(cls, v, values):
        return slugify(
            f'{values["display_name"]} {values["state"]} {values["country"]} {values["elevation"]}'
        )


class Tick(BaseModel):
    climber: str
    date: datetime.date


class InterestedClimber(BaseModel):
    climber: str
