from typing import List

from fastapi import APIRouter, status

from src.apps.chat.schema import Message, MessageOut, ReadMessage
from src.apps.service.chat import ChatService

router = APIRouter(prefix='/message')


@router.post('/', response_model=MessageOut)
async def create_message(message: Message):
    return await ChatService().create_message(message.chat_id, message)


@router.get('/chat/{chat_id}/', response_model=List[MessageOut])
async def get_messages(chat_id: int, message_id: int = 0):
    messages = await ChatService().get_messages(chat_id, message_id)
    return messages


@router.post('/read/', response_model=ReadMessage)
async def create_message(message: ReadMessage):
    return await ChatService().read_message(
        chat_id=message.chat_id,
        user_id=message.user_id,
        message_id=message.message_id,
    )
