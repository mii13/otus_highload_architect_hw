from typing import List

from fastapi import APIRouter, status

from src.services.chat.schema import Message, MessageOut, Chat, ChatOut
from src.services.chat.client import ChatService
from config import settings


message_router = APIRouter(prefix='/message')
chat_router = APIRouter(prefix='/chat')


@message_router.post('/', response_model=MessageOut)
async def create_message(message: Message):
    return await ChatService(settings.chart_service_url).create_message(message)


@message_router.get('/chat/{chat_id}/', response_model=List[MessageOut])
async def get_messages(chat_id: int, message_id: int = 0):
    return await ChatService(settings.chart_service_url).get_messages(chat_id, message_id)


@chat_router.post('/', response_model=ChatOut)
async def create_chat(chat: Chat):
    return await ChatService(settings.chart_service_url).create_chat(chat)


@chat_router.get('/', response_model=List[ChatOut])
async def get_chats(user_id: int):
    return await ChatService(settings.chart_service_url).get_chats(user_id)
