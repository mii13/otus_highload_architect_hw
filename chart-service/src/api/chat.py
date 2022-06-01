from typing import List

from fastapi import APIRouter, status

from src.apps.chat.schema import Chat, ChatOut
from src.apps.service.chat import ChatService

router = APIRouter(prefix='/chat')


@router.post('/', response_model=ChatOut)
async def create_chat(chat: Chat):
    return await ChatService().create_chat(chat)


@router.get('/', response_model=List[ChatOut])
async def get_chats(user_id: int):
    chats = await ChatService().get_chats(user_id)
    return chats
