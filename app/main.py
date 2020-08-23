import uvicorn
from fastapi import FastAPI

from app.database import peaks_db, users_db
from app.database.database_utils import get_db
from app.routers import peaks_router

app = FastAPI()


@app.on_event("startup")
async def start_up_tasks(db=None):
    if db is None:
        db = await get_db()
    await peaks_db.create_peak_index(db)
    await users_db.create_user_indexes(db)


app.include_router(peaks_router.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
