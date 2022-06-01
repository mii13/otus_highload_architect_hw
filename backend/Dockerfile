FROM python:3.10.1-bullseye

COPY docker-app/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code

WORKDIR /code


EXPOSE 8088

ENTRYPOINT ["/entrypoint.sh"]
