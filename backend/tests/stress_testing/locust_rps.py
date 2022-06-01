from locust import HttpUser, task


class AnonymousUser(HttpUser):
    @task(10)
    def get_profiles(self):
        self.client.get(
            '/profiles',
            params={"name": "il", "second_name": "mi"},
        )
