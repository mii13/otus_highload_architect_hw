from fastapi import APIRouter
from src.api.routers import counter

router = APIRouter()

router.include_router(counter.router)
