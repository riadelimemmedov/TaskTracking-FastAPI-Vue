#!/bin/bash

# Run black
poetry run black .

# Run isort
poetry run isort . --profile black

# Run flake8
poetry run flake8 .