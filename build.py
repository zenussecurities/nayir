#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nayiraah_project.settings')
django.setup()

from django.core.management import call_command

# Collect static files
print("Collecting static files...")
call_command('collectstatic', '--noinput')

# Run migrations if DATABASE_URL is set (production)
if os.environ.get('DATABASE_URL'):
    print("Running migrations...")
    call_command('migrate', '--noinput')

print("Build complete!")
