FROM python:3.10-alpine

WORKDIR /root

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY templates ./templates
COPY static ./static
COPY instance ./instance
COPY app.py .

EXPOSE 5000

CMD [ "python3", "./app.py" ]    