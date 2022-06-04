FROM python:3.10.4-bullseye

COPY docker-app/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY ./requirements /code/requirements

RUN pip install --no-cache-dir --no-input -r /code/requirements/base.txt

COPY . /code

WORKDIR /code

EXPOSE 8088

ENTRYPOINT ["/entrypoint.sh"]
