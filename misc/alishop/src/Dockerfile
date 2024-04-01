FROM python:3.10-alpine

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY bot.py .
COPY ./files ./files

CMD python3 bot.py