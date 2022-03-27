from pydantic import BaseModel, EmailStr, constr


class LoginUser(BaseModel):
    email: EmailStr
    password: constr(min_length=5, max_length=100)
