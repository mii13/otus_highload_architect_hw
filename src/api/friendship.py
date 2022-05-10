from fastapi import Depends, Request, APIRouter, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from src.apps.friendship.service import FriendshipService
from src.apps.auth.service import get_current_user

templates = Jinja2Templates(directory='src/templates/')
router = APIRouter(prefix='/friend')


@router.get('/')
async def get_friends(
    request: Request,
    current_user=Depends(get_current_user),
):
    if not current_user:
        return RedirectResponse('auth/login', status_code=302)
    service = FriendshipService()
    friends = await service.get_friends(current_user.id)

    return templates.TemplateResponse(
        'friends.html',
        {'request': request, 'friends': friends},
    )


@router.post('/add')
async def add_friend(
    request: Request,
    current_user=Depends(get_current_user),
    friend: int = Form(...),
):
    if not current_user:
        return RedirectResponse('auth/login', status_code=302)
    service = FriendshipService()
    # todo: add validation
    await service.make_friends(current_user.id, friend)
    friends = await service.get_friends(current_user.id)

    return templates.TemplateResponse(
        'friends.html',
        {'request': request, 'friends': friends},
    )
