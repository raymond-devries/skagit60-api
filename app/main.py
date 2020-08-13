import uvicorn
from fastapi import FastAPI

from app.routers import peaks_router

app = FastAPI()

app.include_router(peaks_router.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
