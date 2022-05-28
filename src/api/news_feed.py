from fastapi import Depends, Request, APIRouter, WebSocket, Cookie
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from src.apps.news_feed.service import NewsFeedService
from src.apps.post.service import PostService
from src.apps.auth.service import get_current_user
from src.api.ws import ws_manager
from config import settings
import logging

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory='src/templates/')
router = APIRouter(prefix='/news_feed')


@router.get('/')
async def get_news_feed(
    request: Request,
    current_user=Depends(get_current_user),
):
    if not current_user:
        return RedirectResponse('auth/login', status_code=302)
    service = NewsFeedService()
    posts = await service.get_posts(current_user.id)

    return templates.TemplateResponse(
        'news_feed.html',
        {'request': request, 'posts': posts},
    )


@router.get('/with_ws')
async def get_news_feed_with_ws(
    request: Request,
    current_user=Depends(get_current_user),
):
    if not current_user:
        return RedirectResponse('auth/login', status_code=302)
    service = NewsFeedService()
    posts = await service.get_posts(current_user.id)

    return templates.TemplateResponse(
        'news_feed_ws.html',
        {
            'request': request,
            'posts': posts,
            'host': settings.web_host,
            'port': settings.web_port,
            'user_id': current_user.id,
        },
    )


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
):
    await ws_manager.connect(user_id, websocket)
    service = PostService()
    while True:
        text = await websocket.receive_text()
        logger.error(f'new message: {text}')
        post = await service.create_post(user_id, text=text)
        await websocket.send_text(
            f"{post.text} ({post.user_name} {post.user_second_name}, {post.created_at})",
        )