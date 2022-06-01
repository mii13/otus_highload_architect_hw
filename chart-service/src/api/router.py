from fastapi import APIRouter

from src.api import chat, message

router = APIRouter(prefix='')

router.include_router(chat.router)
router.include_router(message.router)
