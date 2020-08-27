from typing import List

from fastapi import APIRouter, Depends, Response, status
from pymongo.errors import DuplicateKeyError

from app.database import peaks_db
from app.database.database_utils import get_db
from app.models import peak_model

router = APIRouter()


@router.get("/peaks/", tags=["peaks"], response_model=List[peak_model.PeakWithSlug])
async def get_peaks(db=Depends(get_db)):
    return await peaks_db.get_peaks_db(db)


@router.post(
    "/peak/", tags=["peaks"], response_model=str, status_code=status.HTTP_201_CREATED
)
async def add_peak(peak: peak_model.PeakIn, response: Response, db=Depends(get_db)):
    try:
        return await peaks_db.create_peak_db(peak, db)
    except DuplicateKeyError as e:
        response.status_code = status.HTTP_409_CONFLICT
        return str(e)
