FROM python:3.7-alpine3.7

RUN apk add --no-cache --update bash

RUN adduser -D miniapi

WORKDIR /home/miniapi

COPY blogpostapi blogpostapi
COPY Pipfile Pipfile.lock .env boot.sh ./

RUN chmod +x boot.sh
RUN pip install pipenv
RUN pipenv install --system

RUN chown -R miniapi:miniapi ./
USER miniapi

EXPOSE 5000
CMD ["./boot.sh"]
