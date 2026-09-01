import sys
import os
from io import BytesIO
from pathlib import Path

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
    Converts Vercel's HTTP request to WSGI format and converts WSGI response
    back into a Django HttpResponse so Vercel returns correct status and headers.
    """
    try:
        # Extract request information
        method = request.method
        path = request.path
        query_string = request.query_string or ""

        # Determine scheme from forwarded header (Vercel sets x-forwarded-proto)
        proto = request.headers.get('x-forwarded-proto', '') or request.headers.get('X-Forwarded-Proto', '')
        scheme = 'https' if proto.lower() == 'https' else 'http'

        # Host and port parsing
        host_header = request.headers.get('host', 'localhost')
        if ':' in host_header:
            server_name, server_port = host_header.split(':', 1)
        else:
            server_name = host_header
            server_port = '443' if scheme == 'https' else '80'

        # Build the environ dict for WSGI
        environ = {
            'REQUEST_METHOD': method,
            'SCRIPT_NAME': '',
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': request.headers.get('content-type', ''),
            'CONTENT_LENGTH': request.headers.get('content-length', ''),
            'SERVER_NAME': server_name,
            'SERVER_PORT': server_port,
            'SERVER_PROTOCOL': request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1'),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': scheme,
            'wsgi.input': BytesIO(request.body or b''),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': True,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            # Some frameworks expect REMOTE_ADDR
            'REMOTE_ADDR': request.client.host if getattr(request, 'client', None) else '',
        }

        # Add headers to environ (skip CONTENT_TYPE and CONTENT_LENGTH as WSGI has specific keys)
        for header, value in request.headers.items():
            header_name = header.upper().replace('-', '_')
            if header_name in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                continue
            environ[f'HTTP_{header_name}'] = value

        # start_response capture
        captured = {'status': '200 OK', 'headers': []}
        def start_response(status, response_headers, exc_info=None):
            captured['status'] = status
            captured['headers'] = response_headers
            # WSGI start_response returns a write callable only for legacy apps; we don't need to return it
            return None

        # Call Django WSGI app
        response_iter = django_app(environ, start_response)

        # Build body (response_iter may be an iterable of bytes)
        if hasattr(response_iter, '__iter__') and not isinstance(response_iter, (bytes, bytearray)):
            body = b''.join(item if isinstance(item, (bytes, bytearray)) else str(item).encode('utf-8') for item in response_iter)
        else:
            body = response_iter if isinstance(response_iter, (bytes, bytearray)) else str(response_iter).encode('utf-8')

        # If the WSGI response object has a close() method, call it
        try:
            close_method = getattr(response_iter, 'close', None)
            if callable(close_method):
                close_method()
        except Exception:
            pass

        # Extract status code
        status_code = int(captured['status'].split(' ', 1)[0]) if captured.get('status') else 200

        # Build Django HttpResponse and copy headers
        resp = HttpResponse(body, status=status_code)
        for header_name, header_value in captured.get('headers', []):
            # Skip hop-by-hop headers that should not be forwarded
            if header_name.lower() in ('transfer-encoding', 'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers', 'upgrade'):
                continue
            resp[header_name] = header_value

        return resp

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
