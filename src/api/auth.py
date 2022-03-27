from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Depends, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from starlette.responses import RedirectResponse

from src.apps.auth import service
from src.apps.user.repository import UserRepository
from src.apps.user.schemas import Registration
from src.apps.auth.schemas import LoginUser


templates = Jinja2Templates(directory='src/templates/')
router = APIRouter(prefix='/auth', tags=['employee'])


async def registration_data(
    name: str = Form(...),
    second_name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    city: str = Form(...),
    interests: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    return dict(
        name=name,
        second_name=second_name,
        age=age,
        gender=gender,
        city=city,
        interests=interests,
        email=email,
        password=password,
    )


async def login_data(email: str = Form(...), password: str = Form(...)):
    return dict(email=email, password=password)


@router.get('/login')
def login_get(
    request: Request,
    current_user=Depends(service.get_current_user),
):
    if current_user:
        return RedirectResponse('/me', status_code=302)
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/logout')
def logout():
    response = RedirectResponse('login', status_code=302)
    response.delete_cookie('Authorization')
    return response


@router.post('/login')
async def login_post(
    request: Request,
    form_data: dict = Depends(login_data),
):
    try:
        login_user = LoginUser(**form_data)
    except ValidationError as er:
        return templates.TemplateResponse(
            'login.html',
            {'request': request, 'er': er},
        )
    user = await service.authenticate_user(login_user.email, login_user.password)
    if not user:
        return templates.TemplateResponse(
            'login.html',
            {'request': request, 'er': 'email/password incorrect'},
    )
    response = RedirectResponse('/me', status_code=302)
    token = service.create_access_token({'email': user.email})
    response.set_cookie(
        'Authorization',
        value=f'Bearer {token}',
        httponly=True,
        max_age=24 * 60 * 60,
        expires=24 * 60 * 60,
    )
    return response


@router.get('/registration', response_class=HTMLResponse)
async def registration_get(
    request: Request,
    current_user=Depends(service.get_current_user),
):
    if current_user:
        return RedirectResponse('/me', status_code=302)
    return templates.TemplateResponse(
        'registration.html',
        {'request': request},
    )


@router.post('/registration', response_class=HTMLResponse)
async def registration_post(
    request: Request,
    current_user=Depends(service.get_current_user),
    form_data: dict = Depends(registration_data),
):
    user_repo = UserRepository()
    if current_user:
        return RedirectResponse('/me', status_code=302)
    try:
        new_user = Registration(**form_data)
    except ValidationError as er:
        return templates.TemplateResponse(
            'registration.html',
            {'request': request, 'er': er},
        )
    exist_user = await user_repo.get_user(new_user.email)
    if exist_user:
        return templates.TemplateResponse(
            'registration.html',
            {'request': request, 'er': f'user with email {new_user.email} already exist'},
        )

    await user_repo.add_user(
        new_user.name, new_user.second_name, new_user.age, new_user.gender,
        new_user.city, new_user.interests, new_user.email, new_user.password,
    )

    return templates.TemplateResponse(
        'registration_success.html',
        {'request': request},
    )