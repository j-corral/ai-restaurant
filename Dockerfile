FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m venv /opt/venv && . /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

COPY ./alembic ./alembic
COPY ./app ./app
COPY ./scripts ./scripts

COPY .env .env
COPY alembic.ini .

RUN chmod +x ./scripts/entrypoint.sh


ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["./scripts/entrypoint.sh"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]