#!/bin/bash

# Navigate to your Django project root first
# Usage: ./clean_migrations.sh

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
