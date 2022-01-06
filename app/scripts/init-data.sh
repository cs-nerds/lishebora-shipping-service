#!/bin/bash

alembic upgrade head

python app/initial.py