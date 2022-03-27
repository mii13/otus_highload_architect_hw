import asyncio
import sys
import os

from faker import Faker
from pathlib import Path

print(sys.path)
path = os.path.join(Path('.').absolute(), 'src')
print(path)
sys.path.append(
    # Path('.').absolute().parent,
    path
)
sys.path.append(
    # Path('.').absolute().parent,
    os.path.join(path, '..'),
)
print(sys.path)
from src.user.repository import UserRepository
from src.user.enums import Gender


interests = ['football', 'hockey', 'music', 'reading of books']

N = 1_000_000


def generate_profiles(count):
    fake = Faker()
    for _ in range(count):
        profile = fake.profile()
        if profile['sex'].lower() == Gender.male:
            gender = Gender.male
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
        else:
            gender = Gender.female
            first_name = fake.first_name_female()
            last_name = fake.last_name_female()

        yield {
            'name': first_name,
            'second_name': last_name,
            'gender': gender,
            'age': fake.pyint(18, 100),
            'city': fake.city(),
            'email': fake.unique.email(),
            'interests': interests[fake.pyint(0, len(interests) - 1)],
            'password': fake.password(),
        }


async def create(count):
    repository = UserRepository()
    for user in generate_profiles(count):
        await repository.add_user(**user)


if __name__ == '__main__':
    asyncio.run(create(N))
