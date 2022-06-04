## Миграции
1. Просмотр изменений:
```shell
alembic revision --message="init models" --autogenerate 
``` 
или через docker-compose, но на созданные файлы права будут уже другие. Можно потом применить chown.
```shell
docker-compose -f ./docker-compose.yml run --rm api  "alembic revision --autogenerate"
``` 
2. Применение миграций
```shell
alembic upgrade head
```
или через docker-compose
```shell
docker-compose -f ./docker-compose.yml run --rm api  "alembic upgrade head"
``` 
