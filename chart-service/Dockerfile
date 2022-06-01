FROM python:3.10.1-bullseye

COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code

WORKDIR /code

EXPOSE 8088

CMD python db_migrate.py && opentelemetry-instrument uvicorn main:app --port 8088 --host "0.0.0.0" --reload