FROM gliderlabs/alpine:3.1

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
    supervisor \
  && rm -rf /var/cache/apk/*

COPY requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt

ADD supervisord.conf /etc/supervisord.conf
ADD . /code

CMD ["/usr/bin/supervisord"]
