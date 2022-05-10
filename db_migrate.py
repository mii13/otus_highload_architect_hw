import asyncio
from src.database.migrations import run


if __name__ == '__main__':
    asyncio.run(run.init())
