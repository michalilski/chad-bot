from fastapi import APIRouter

from app.v1.chat import router as chat_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat")


@router.get("/")
async def root():
    return {"message": "Version 1 API root directory. See API docs for details."}
