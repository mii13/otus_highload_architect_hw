from src.apps.chat.schema import Message
from src.apps.repository.chat import ChatRepository
from src.apps.providers.counter import CounterClient, SagaError
from src.settings import settings


class ChatService:
    def __init__(self):
        self.repository = ChatRepository()

    async def create_message(self, chat_id, message: Message):
        await CounterClient(settings.counter_url).increment(
            chat_id=message.chat_id,
            user_id=message.user_id,
        )
        try:
            message = await self.repository.create_message(chat_id, message)
        except Exception:
            # saga rollback
            await CounterClient(settings.counter_url).decrement(
                chat_id=message.chat_id,
                user_id=message.user_id,
            )
        return message

    async def get_messages(self, chat_id, from_message_id):
        return await self.repository.get_messages(chat_id, from_message_id)

    async def read_message(self, chat_id: int, user_id: int, message_id: int):

        await self.repository.set_offset(chat_id, user_id, message_id)
        message_cnt = await self.repository.message_count(chat_id, user_id, message_id)
        await CounterClient(settings.counter_url).decrement(
            chat_id=chat_id,
            user_id=user_id,
            cnt=message_cnt,
        )

    async def get_chats(self, user_id: int):
        counter = await CounterClient(settings.counter_url).list(user_id=user_id)
        counter = {chat['chat_id']: chat['count'] for chat in counter}
        chats = await self.repository.get_chats(user_id)
        for chat in chats:
            chat['unread'] = counter.get(chat['id'], 0)
        return chats

    async def create_chat(self, chat):
        created_chat = await self.repository.create_chat(chat.name)
        for user in chat.users:
            await self.repository.create_participant(created_chat['id'], user)
        return created_chat
