"""
WSGI entry point for the Tutorial Resource Management application.

Used by:
    - `flask --app wsgi:app` CLI commands (run, db migrate, etc.)
    - Production WSGI servers (gunicorn, waitress): ``gunicorn wsgi:app``

The ``app`` object is created via the application factory in ``web.create_app``.
"""

from web import create_app

# Application instance consumed by Flask CLI and WSGI servers
app = create_app()
