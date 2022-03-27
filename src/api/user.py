from fastapi import Depends, Request, APIRouter
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from src.apps.user.repository import UserRepository
from src.apps.auth.service import get_current_user

templates = Jinja2Templates(directory='src/templates/')

router = APIRouter()


@router.get('/')
async def root():
    return RedirectResponse('/me', status_code=302)


@router.get('/profiles')
async def profiles(name: str = '', second_name: str = '', limit: int = 10, offset: int = 0):
    user_repo = UserRepository()
    users = await user_repo.search_profiles(name, second_name, limit, offset)
    return users


@router.get('/me')
async def me(
    request: Request,
    current_user=Depends(get_current_user),
):
    if not current_user:
        return RedirectResponse('auth/login', status_code=302)
    return templates.TemplateResponse(
        'me.html',
        {'request': request, 'user': current_user},
    )
