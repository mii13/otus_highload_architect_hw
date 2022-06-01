from typing import List
import json
from datetime import datetime
from typing import NamedTuple


class Post(NamedTuple):
    id: int
    user_id: int
    text: str
    created_at: datetime
    user_name: str
    user_second_name: str


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


def serialize_post(posts: List[Post]):
    return json.dumps(
        [
            {
                "id": post.id,
                "user_id": post.user_id,
                "user_name": post.user_name,
                "user_second_name": post.user_second_name,
                "text": post.text,
                "created_at": post.created_at,
            }
            for post in posts
        ],
        cls=CustomJsonEncoder,
    )


def deserialize_posts(posts: str) -> List[Post]:
    res = []
    for row in json.loads(posts):
        row['created_at'] = datetime.fromisoformat(row['created_at'])
        res.append(Post(**row))
    return res


def deserialize_post(post: str) -> Post:
    return Post(**json.loads(post))
