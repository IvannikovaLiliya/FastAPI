FROM python:3.11-slim as builder

WORKDIR /app
COPY . .

RUN python3 -m pip install -r requirements_correct.txt

CMD ["python", "./main.py"]