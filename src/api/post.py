from fastapi import Depends, Request, APIRouter, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from src.apps.post.service import PostService
from src.apps.auth.service import get_current_user

templates = Jinja2Templates(directory='src/templates/')
router = APIRouter(prefix='/posts')


@router.post('/')
async def create_post(
    request: Request,
    current_user=Depends(get_current_user),
    text: str = Form(...),
):
    if not current_user:
        return RedirectResponse('auth/login', status_code=302)
    service = PostService()
    await service.create_post(current_user.id, text)
    return templates.TemplateResponse(
        'post_create_success.html',
        {'request': request},
    )
