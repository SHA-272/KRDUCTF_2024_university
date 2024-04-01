FROM python:3.10-slim

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY instance/users.db ./instance/users.db
COPY app.py .

EXPOSE 5000

CMD gunicorn app:"app" -b 0.0.0.0:5000 --reload