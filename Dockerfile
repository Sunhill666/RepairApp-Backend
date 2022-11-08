FROM python:3.9.13-alpine

ADD . /project
WORKDIR /project

EXPOSE 8000

RUN apk add --update --no-cache build-base mariadb-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-base --purge && \
    chmod +x ./startup.sh

CMD ["./startup.sh"]