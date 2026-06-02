FROM python:3.12-slim

WORKDIR /managing_cost

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/managing_cost \
    PORT=8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic -c core/alembic.ini upgrade head && uvicorn core.main:app --host 0.0.0.0 --port ${PORT}"]
