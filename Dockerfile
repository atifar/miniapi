FROM python:3.7-alpine3.7

RUN adduser -D miniapi

WORKDIR /home/miniapi

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY blogpostapi blogpostapi
COPY boot.sh ./
RUN chmod +x boot.sh

RUN chown -R miniapi:miniapi ./
USER miniapi

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
