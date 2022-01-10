import jwt
from fastapi import Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from jwt import PyJWTError
from pydantic import ValidationError
from starlette.responses import RedirectResponse

from app import app
from src.user.repository import User, UserRepository
from src.user.schemas import LoginUser, Registration

templates = Jinja2Templates(directory='templates/')

SECRET_KEY = 'aee1006e3fab455cd7289b6607be3124c7b1ffa42c1b2bbed6ba2d0ba03e5b35'
ALGORITHM = 'HS256'


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


def check_user_password(user: User, password):
    # ToDo: use hash
    return user.password == password


def get_token(request):
    cookie_authorization: str = request.cookies.get('Authorization')
    cookie_scheme, cookie_param = get_authorization_scheme_param(
        cookie_authorization
    )
    param = None

    if cookie_scheme.lower() == 'bearer':
        param = cookie_param

    return param


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request):
    token = get_token(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('email')
        if email is None:
            return None
    except PyJWTError:
        return None
    user_repo = UserRepository()
    user = await user_repo.get_user(email)
    return user


@app.get('/me')
async def me(
    request: Request,
    current_user=Depends(get_current_user),
):
    if not current_user:
        return RedirectResponse('/login', status_code=302)
    return templates.TemplateResponse(
        'me.html',
        {'request': request, 'user': current_user},
    )


def get_user_token(user: User):
    return f'token-{user.id}'


@app.get('/login')
def login_get(
    request: Request,
    current_user=Depends(get_current_user),
):
    if current_user:
        return RedirectResponse('/me', status_code=302)
    return templates.TemplateResponse('login.html', {'request': request})


@app.post('/logout')
def logout():
    response = RedirectResponse('/login', status_code=302)
    response.delete_cookie('Authorization')
    return response


@app.post('/login')
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
    user_repo = UserRepository()
    user = await user_repo.get_user(login_user.email)

    if not user or not check_user_password(user, login_user.password):
        return templates.TemplateResponse(
            'login.html',
            {'request': request, 'er': 'email/password incorrect'},
    )
    response = RedirectResponse('/me', status_code=302)
    token = create_access_token({'email': user.email})
    response.set_cookie(
        'Authorization',
        value=f'Bearer {token}',
        httponly=True,
        max_age=24 * 60 * 60,
        expires=24 * 60 * 60,
    )
    return response


@app.get('/registration', response_class=HTMLResponse)
async def registration_get(
    request: Request,
    current_user=Depends(get_current_user),
):
    if current_user:
        return RedirectResponse('/me', status_code=302)
    return templates.TemplateResponse(
        'registration.html',
        {'request': request},
    )


@app.post('/registration', response_class=HTMLResponse)
async def registration_post(
    request: Request,
    current_user=Depends(get_current_user),
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

    return templates.TemplateResponse('registration_success.html', {'request': request})
