FROM python:3.8
LABEL maintainer 'Victor'
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT True

RUN mkdir /app
WORKDIR /app

COPY Pipfile /app/
COPY Pipfile.lock /app/

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app/

WORKDIR /app
