from typing import Optional
import jwt
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from jwt import PyJWTError
from src.apps.user.repository import UserRepository
from src.apps.user.containers import User

SECRET_KEY = 'aee1006e3fab455cd7289b6607be3124c7b1ffa42c1b2bbed6ba2d0ba03e5b35'
ALGORITHM = 'HS256'


async def authenticate_user(email, password) -> Optional[User]:
    """Аутентификация пользователя."""
    user_repo = UserRepository()
    user = await user_repo.get_user(email)
    if not user or not check_user_password(user, password):
        return None
    return user


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


def check_user_password(user: User, password):
    # ToDo: use hash
    return user.password == password


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
