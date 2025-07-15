FROM python:3.11-slim

WORKDIR /app
COPY checker.py .

RUN pip install requests

CMD ["sleep", "infinity"]
