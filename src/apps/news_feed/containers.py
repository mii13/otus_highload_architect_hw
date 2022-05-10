from datetime import datetime
from typing import NamedTuple


class NewsPost(NamedTuple):
    id: int
    user_id: int
    user_name: str
    user_second_name: str
    text: str
    created_at: datetime
