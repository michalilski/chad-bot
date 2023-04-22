from fastapi import FastAPI

from app.v1.api import router as v1_router

app = FastAPI()
app.include_router(v1_router, prefix="/v1")
