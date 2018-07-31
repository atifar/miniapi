FROM python:3.7-alpine3.7

RUN apk add --no-cache --update bash

RUN adduser -D miniapi

WORKDIR /home/miniapi

COPY Pipfile Pipfile.lock .env ./

RUN pip install pipenv
RUN pipenv install --system

COPY blogpostapi blogpostapi

RUN chown -R miniapi:miniapi ./
USER miniapi

EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "blogpostapi:app"]
