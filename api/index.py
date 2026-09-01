import os
import sys
from pathlib import Path

# Add project root directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Load settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nayiraah_project.settings')

# Import Django WSGI application for Vercel
from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
