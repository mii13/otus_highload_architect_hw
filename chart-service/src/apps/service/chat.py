from src.apps.chat.schema import Message
from src.apps.repository.chat import ChatRepository


class ChatService:
    def __init__(self):
        self.repository = ChatRepository()

    async def create_message(self, chat_id, message: Message):
        return await self.repository.create_message(chat_id, message)

    async def get_messages(self, chat_id, from_message_id):
        return await self.repository.get_messages(chat_id, from_message_id)

    async def read_message(self, chat_id, message_id: int):
        ...

    async def get_chats(self, user_id):
        return await self.repository.get_chats(user_id)

    async def create_chat(self, chat):
        created_chat = await self.repository.create_chat(chat.name)
        for user in chat.users:
            await self.repository.create_participant(created_chat['id'], user)
        return created_chat
