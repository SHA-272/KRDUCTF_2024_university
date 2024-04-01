FROM python:3.10-alpine

WORKDIR /root

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD gunicorn app:"app" -b 0.0.0.0:5000 --reload  