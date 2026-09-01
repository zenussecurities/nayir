import sys
import os
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlparse

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nayiraah_project.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

# Get the WSGI application
django_app = get_wsgi_application()

def handler(request):
    """
    Vercel serverless function handler for Django.
    Converts Vercel's HTTP request to WSGI format.
    """
    try:
        # Extract request information
        method = request.method
        path = request.path
        query_string = request.query_string or ""
        
        # Build the environ dict for WSGI
        environ = {
            'REQUEST_METHOD': method,
            'SCRIPT_NAME': '',
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': request.headers.get('content-type', ''),
            'CONTENT_LENGTH': request.headers.get('content-length', ''),
            'SERVER_NAME': request.headers.get('host', 'localhost').split(':')[0],
            'SERVER_PORT': request.headers.get('host', 'localhost:80').split(':')[1] if ':' in request.headers.get('host', '') else '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https' if request.headers.get('x-forwarded-proto') == 'https' else 'http',
            'wsgi.input': BytesIO(request.body or b''),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': True,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }
        
        # Add headers to environ
        for header, value in request.headers.items():
            header = header.upper().replace('-', '_')
            if header not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                environ[f'HTTP_{header}'] = value
        
        # Call Django WSGI app
        response = django_app(environ, start_response)
        
        # Convert WSGI response to Vercel response
        if hasattr(response, '__iter__'):
            body = b''.join(response)
        else:
            body = response
            
        return HttpResponse(body, status=200)
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def start_response(status, response_headers, exc_info=None):
    """WSGI start_response callable."""
    pass
