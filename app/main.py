import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import peaks_db, users_db
from app.database.database_utils import get_db
from app.routers import peaks_router, user_router

app = FastAPI()

origins = ["http://localhost", "http://localhost:8080", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_up_tasks(db=None):
    if db is None:
        db = await get_db()
    await peaks_db.create_peak_index(db)
    await users_db.create_user_indexes(db)


app.include_router(peaks_router.router)
app.include_router(user_router.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
