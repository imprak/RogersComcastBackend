#!/bin/bash
./scripts/wait-for-db.sh

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4