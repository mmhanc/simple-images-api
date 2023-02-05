from .base import *

import tempfile


DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'app_db_test'
    }
}

MEDIA_ROOT = tempfile.mkdtemp()
