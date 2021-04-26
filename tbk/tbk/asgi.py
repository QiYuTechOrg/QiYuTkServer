"""
ASGI config for tbk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

import dotenv
from django.core.asgi import get_asgi_application

__all__ = ["app"]

dot_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../.env")
if os.path.exists(dot_file):
    dotenv.read_dotenv(dot_file)

os.environ.setdefault("WS_DJANGO_RUN_MODE", "async")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tbk.settings")

application = get_asgi_application()

from core.api import app  # noqa

api_app = app
