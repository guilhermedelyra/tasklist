FROM python:3.8.1-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 5000
WORKDIR /usr/app


RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.in-project false
RUN poetry install

COPY . ./

CMD poetry run flask run --host=0.0.0.0