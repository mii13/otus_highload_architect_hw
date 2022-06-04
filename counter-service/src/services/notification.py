from src.repositories.notification import Notification, NotificationRepository
from src.repositories.notification_item import NotificationItemRepository
from src.repositories.notification_type import NotificationTypeRepository
from src.repositories.subscription import SubscriptionRepository
from src.schemas.notification import NotificationWrite
from src.services.exception import TypeNotFoundException


class NotificationService:
    def __init__(self, session):
        self.session = session
        self.repository = NotificationRepository(session)
        self.type_repository = NotificationTypeRepository(session)
        self.item_repository = NotificationItemRepository(session)

    async def get(self, notification_id):
        return await self.repository.get(notification_id)

    async def list(
        self,
        employee_id: int | None,
        device_name: str | None,
        limit: int | None,
        offset: int | None,
    ) -> list[Notification]:
        return await self.repository.list(employee_id, device_name, limit, offset)

    async def create(self, notification: NotificationWrite) -> Notification:
        subscription_repo = SubscriptionRepository(self.session)
        _type = await self.type_repository.get_by_code(notification.type_code)
        if _type is None:
            raise TypeNotFoundException()
        notification_obj = await self.repository.create(_type, notification)
        subscribers = await subscription_repo.get_subscribers(type_id=_type.id)
        for subscriber in subscribers:
            for channel in subscriber.channels:
                await self.item_repository.create(
                    user_id=subscriber.user_id,
                    notification_id=notification_obj.id,
                    channel=channel,
                )

        return notification_obj
