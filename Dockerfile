FROM gliderlabs/alpine:3.1

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && rm -rf /var/cache/apk/*

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY tutum-schedule.py /code/tutum-schedule.py

CMD ["/usr/bin/python", "/code/tutum-schedule.py"]
