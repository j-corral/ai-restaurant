FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m venv /opt/venv && . /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

COPY ./app ./app
COPY .env .env

ENV PATH="/opt/venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]