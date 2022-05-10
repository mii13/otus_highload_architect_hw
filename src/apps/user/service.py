from .repository import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_by_id(self, user_id: int):
        return self.repository.get_user_by_id(user_id)
