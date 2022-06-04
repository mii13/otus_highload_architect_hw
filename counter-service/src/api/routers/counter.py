from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.repositories.counter import CounterRepository
from src.api.dependencies.repository import get_repository
from src.schemas.counter import CounterSchema

router = APIRouter(prefix="/counter", tags=["counter"])


@router.get(
    "/{user_id}/",
    name="get_counter_list",
    response_model=List[CounterSchema],
)
async def get_counter_list(
    user_id: int,
    repository: CounterRepository = Depends(get_repository(CounterRepository)),
):
    return await repository.list(user_id)


@router.get(
    "/{user_id}/{chat_id}/",
    name="get_counter",
    response_model=CounterSchema,
)
async def get_counter(
    user_id: int,
    chat_id: int,
    repository: CounterRepository = Depends(get_repository(CounterRepository)),
):
    counter = await repository.get(user_id, chat_id)
    if counter is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return counter


@router.post(
    "/inc/",
    name="inc_counter",
    response_model=CounterSchema,
    status_code=status.HTTP_201_CREATED,
)
async def inc_counter(
    counter: CounterSchema,
    repository: CounterRepository = Depends(get_repository(CounterRepository)),
):
    return await repository.append(counter)


@router.post(
    "/dec/",
    name="dec_counter",
    response_model=CounterSchema,
    status_code=status.HTTP_201_CREATED,
)
async def dec_counter(
    counter: CounterSchema,
    repository: CounterRepository = Depends(get_repository(CounterRepository)),
):
    return await repository.decrement(counter)
