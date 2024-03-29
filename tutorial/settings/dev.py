from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y&3pt&=ve*ua_n)ry*yhl6)y#n^t#b*47mh_@sdp6x6!&*&21@'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += ['django_extensions']

try:
    from .local import *
except ImportError:
    pass
