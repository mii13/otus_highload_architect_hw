from fastapi import APIRouter

from src.api import auth, user, friendship, post, news_feed

router = APIRouter(prefix='')

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(friendship.router)
router.include_router(post.router)
router.include_router(news_feed.router)
