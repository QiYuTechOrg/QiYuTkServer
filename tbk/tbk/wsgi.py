"""
WSGI config for tbk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

import dotenv
from django.core.wsgi import get_wsgi_application

dot_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../.env")
if os.path.exists(dot_file):
    dotenv.read_dotenv(dot_file)

os.environ.setdefault("WS_DJANGO_RUN_MODE", "sync")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tbk.settings")

application = get_wsgi_application()
