from locust import HttpUser, task


class AnonymousUser(HttpUser):
    @task(10)
    def get_chats(self):
        self.client.get(
            '/message/chat/1/',
        )

    @task(10)
    def get_messages(self):
        self.client.get(
            '/chat/',
            params={"user_id": "1"},
        )
