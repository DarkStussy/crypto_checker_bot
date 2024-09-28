#!/bin/sh

alembic upgrade head

exec python3 -m crypto_checker