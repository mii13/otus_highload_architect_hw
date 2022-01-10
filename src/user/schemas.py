from pydantic import BaseModel, EmailStr, conint, constr

from .enums import Gender


class LoginUser(BaseModel):
    email: EmailStr
    password: constr(min_length=5, max_length=100)


class Registration(BaseModel):
    name: constr(min_length=2, max_length=100)
    second_name: constr(min_length=2, max_length=100)
    age: conint(gt=15, lt=150)
    gender: Gender
    city: constr(min_length=1, max_length=200)
    interests: constr(min_length=1)
    email: EmailStr
    password: constr(min_length=5, max_length=100)

