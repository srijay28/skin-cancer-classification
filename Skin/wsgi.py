"""
WSGI config for Skin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Skin.settings')

application = get_wsgi_application()

