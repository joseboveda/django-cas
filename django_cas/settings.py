"""Django CAS 1.0/2.0 authentication backend"""

from django.conf import settings

__all__ = []

_DEFAULTS = {
    'CAS_ADMIN_PREFIX': None,
    'CAS_EXTRA_LOGIN_PARAMS': None,
    'CAS_IGNORE_REFERER': False,
    'CAS_LOGOUT_COMPLETELY': True,
    'CAS_REDIRECT_URL': '/',
    'CAS_RETRY_LOGIN': False,
    'CAS_PROXY_CALLBACK': None,
    'CAS_SERVER_URL': None,
    'CAS_VERSION': '2',
}

CAS_URI = 'http://www.yale.edu/tp/cas'
CAS = '{%s}' % CAS_URI

for key, value in _DEFAULTS.iteritems():
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError:
        pass
