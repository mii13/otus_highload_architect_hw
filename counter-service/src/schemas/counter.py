from pydantic import BaseModel


class CounterSchema(BaseModel):
    user_id: int
    chat_id: int
    count: int

    class Config:
        orm_mode = True
