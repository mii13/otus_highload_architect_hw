from datetime import datetime, timezone
from src.apps.chat.schema import Message
from src.apps.repository.base import BaseRepository


class ChatRepository(BaseRepository):
    async def create_message(self, chat_id, message: Message):
        # FixMe: get created dt from client
        create_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        query = """
        insert into message(chat_id, user_id, created_at, text) 
        values (%s, %s, %s, %s)
        """
        args = (
            chat_id, message.user_id, create_dt, message.text,
        )
        message_id = await self.insert_to_shard(chat_id, query, args)
        return {
            "message_id": message_id,
            "created_at": create_dt,
            "chat_id": chat_id,
            "user_id": message.user_id,
            "text": message.text,
        }

    async def delete_message(self, chat_id, message_id: int):
        query = """
        delete from message 
        where id = %s
        """
        args = (message_id, )
        await self.do_query_in_shard(chat_id, query, args)

    async def get_messages(self, chat_id, from_message_id):
        query = """
            select id, chat_id, user_id, text, created_at
            from message
            where id >= %s
            and chat_id = %s
        """
        rows = await self.do_query_in_shard(
            chat_id,
            query,
            (from_message_id, chat_id),
        )
        return [
            {
                'message_id': row[0],
                'chat_id': row[1],
                'user_id': row[2],
                'text': row[3],
                'created_at': row[4],
            }
            for row in rows
        ]

    async def create_chat(self, name: str):
        create_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        query = """
        insert into chat(name, created_at) 
        values (%s, %s)
        """
        args = (
            name, create_dt,
        )
        chat_id = await self.insert(query, args)
        return {
            'id': chat_id,
            'name': name,
        }

    async def message_count(self, chat_id: int, user_id: int, message_id: int):
        query = """
            select count(1)
            from message
            where id >= %s
            and chat_id = %s
            and user_id=%s
        """
        args = (message_id, chat_id, user_id)
        for row in await self.do_query_in_shard(chat_id, query, args):
            return row[0]

    async def get_chats(self, user_id: int):
        query = """
        select chat.id, name from chat inner join participant on chat_id = chat.id
        where user_id = %s
        """
        args = (user_id, )
        chats = await self.do_query(query, args)
        return [
            {
                'id': int(chat[0]),
                'name': chat[1],
            }
            for chat in chats
        ]

    async def create_participant(self, chat_id: int, user: int):
        query = """
        insert into participant(chat_id, user_id) 
        values (%s, %s)
        """
        args = (chat_id, user)
        participant_id = await self.insert(query, args)
        return {
            'id': participant_id,
            'chat_id': chat_id,
            'user_id': user,
        }

    async def get_participants(self, chat_id: int):
        query = """
            select user_id, chat_id, last_read_message
            from participant 
            where chat_id = %s
        """
        args = (chat_id, )
        rows = await self.do_query(query, args)
        return [
            {
                'user_id': row[0],
                'chat_id': row[1],
                'last_read_message': row[2],
            }
            for row in rows
        ]

    async def set_offset(self, chat_id: int, user_id: int, message_id: int):
        query = """
            update participant set last_read_message=%s
            where chat_id=%s
            and user_id=%s 
        """
        args = (message_id, chat_id, user_id)
        await self.do_query(query, args)

    async def get_offset(self, chat_id: int, user_id: int) -> dict | None:
        query = """
            select user_id, chat_id, last_read_message
            from participant 
            where chat_id=%s
            and user_id=%s 
        """
        args = (chat_id, user_id)
        for row in self.do_query(query, args):
            return {
                'user_id': row[0],
                'chat_id': row[1],
                'last_read_message': row[2],
            }
