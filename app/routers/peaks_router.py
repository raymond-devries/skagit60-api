from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import peaks_db
from app.database.database_utils import clean_results, get_db
from app.models import peak_model

router = APIRouter()


# noinspection PydanticTypeCheck
@router.get("/peaks/", tags=["peaks"], response_model=List[peak_model.PeakInDB])
async def get_peaks(db: AsyncIOMotorDatabase = Depends(get_db)):
    results = await peaks_db.get_peaks_db(db)
    return clean_results(results)


@router.post("/peak/", tags=["peaks"])
async def add_peak(peak: peak_model.Peak, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await peaks_db.create_peak_db(peak, db)
