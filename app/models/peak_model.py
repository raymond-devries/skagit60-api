import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, validator
from slugify import slugify

from app.models.custom_types import PydanticObjectId


class PeakIn(BaseModel):
    name: str = Field(max_length=100, example="Baker, Mount")
    display_name: str = Field(max_length=100, example="Mount Baker")
    elevation: int = Field(le=30000, example=10781)
    lat: float = Field(ge=-90, le=90, example=48.77670)
    long: float = Field(ge=-180, le=180, example=-121.81440)
    state: str = Field(max_length=50, example="WA")
    country: str = Field(min_length=2, max_length=3, example="USA")
    peakbagger_link: HttpUrl = Field(
        example="https://www.peakbagger.com/peak.aspx?pid=1633"
    )


class PeakWithSlug(PeakIn):
    slug: Optional[str] = None

    @validator("slug", pre=True, always=True)
    def create_slug(cls, v, values):
        return slugify(
            f'{values["display_name"]} {values["state"]} {values["country"]} '
            f'{values["elevation"]}'
        )


class PeakOut(PeakWithSlug):
    id: PydanticObjectId = Field(example="5f39bd96c746784360738e72", alias="_id")


class Tick(BaseModel):
    climber: str
    date: datetime.date


class InterestedClimber(BaseModel):
    climber: str
