# config.py

import os

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASS', 'password')
DB_NAME = os.getenv('DB_NAME', 'rates')
