from typing import NamedTuple


class Profile(NamedTuple):
    id: int
    email: str
    name: str
    second_name: str
    age: int
    gender: str
    interests: str
    city: str


class User(NamedTuple):
    id: int
    email: str
    name: str
    second_name: str
    age: int
    gender: str
    interests: str
    city: str
    password: str
