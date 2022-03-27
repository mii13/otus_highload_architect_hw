from fastapi import APIRouter

from src.api import auth, user

router = APIRouter(prefix='')

router.include_router(auth.router)
router.include_router(user.router)
