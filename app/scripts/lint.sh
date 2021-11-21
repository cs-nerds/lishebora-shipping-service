#!/bin/bash

mypy app
black app --check
isort --recursive --check-only app
flake8