import os
import sys
import logging
from pathlib import Path

# Add project root directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Load settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nayiraah_project.settings')

import django
django.setup()

from django.core.management import call_command
from django.db import connection

# Ensure database tables exist (for SQLite or fresh serverless instances)
try:
    tables = connection.introspection.table_names()
    if 'core_resource' not in tables:
        logging.info("Initializing database tables and initial data...")
        call_command('migrate', interactive=False)
        try:
            call_command('loaddata', 'initial_data')
        except Exception as fixture_err:
            logging.warning(f"Fixture load skipped/failed: {fixture_err}")
except Exception as db_err:
    logging.error(f"Database setup error: {db_err}")

# Import Django WSGI application for Vercel
from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
