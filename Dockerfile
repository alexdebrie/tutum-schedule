FROM python:2.7.10

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY tutum-schedule.py /code/tutum-schedule.py

CMD python /code/tutum-schedule.py
