from src.apps.chat.schema import Message
from src.apps.repository.chat import ChatRepository
from src.apps.providers.counter import CounterClient, CounterTransactionError
from src.settings import settings


class ChatService:
    def __init__(self):
        self.repository = ChatRepository()

    async def create_message(self, chat_id, message: Message):
        db_message = await self.repository.create_message(chat_id, message)
        participants = await self.repository.get_participants(chat_id)
        success = []
        is_fail = False
        for participant in participants:
            if message.user_id == participant['user_id']:
                continue
            try:
                # todo: add retry
                await CounterClient(settings.counter_url).increment(
                    chat_id=message.chat_id,
                    user_id=participant['user_id'],
                )
            except CounterTransactionError:
                is_fail = True
                break
            success.append(participant['user_id'])

        # rollback
        if is_fail:
            for user_id in success:
                # todo: add retry
                await CounterClient(settings.counter_url).decrement(
                    chat_id=message.chat_id,
                    user_id=user_id,
                )
            await self.repository.delete_message(message.chat_id, db_message['message_id'])
            raise Exception()
        return db_message

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
        created_chat['unread'] = 0
        for user in chat.users:
            await self.repository.create_participant(created_chat['id'], user)
        return created_chat
