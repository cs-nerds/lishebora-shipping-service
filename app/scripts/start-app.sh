#!/bin/bash

alembic upgrade head && bash scripts/init-data.sh && uvicorn main:app --port 80 --host 0.0.0.0