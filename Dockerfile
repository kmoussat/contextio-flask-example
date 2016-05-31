FROM alpine:3.3

RUN apk add --no-cache python && \
    apk add --no-cache --virtual=build-dependencies wget ca-certificates && \
    wget "https://bootstrap.pypa.io/get-pip.py" -O /dev/stdout | python && \
    apk del build-dependencies

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /opt/app

WORKDIR /opt/app

CMD ["python", "app.py"]
