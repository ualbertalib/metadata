 #!/home/ubuntu/anaconda3/bin/python

"""
WSGI config for BIBFRAME_Converter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import django

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BIBFRAME_Converter.settings')

application = get_wsgi_application()
