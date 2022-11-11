FROM python:3.9.13-alpine

ADD . /project
WORKDIR /project

EXPOSE 8000

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add --update --no-cache build-base mariadb-dev && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    apk del build-base --purge && \
    chmod +x ./startup.sh

CMD ["./startup.sh"]