import os
import random
import string

# Defaults for testing. You can replace them here or add a test_config.py
CAS_SERVER_URL = 'https://my.sso.server/'
APP_URL = 'http://my.client.application/'
APP_RESTRICTED = 'restricted'
PROXY_URL = 'https://my.proxy.application/'
# Depending on your cas login form you may need to adjust these field name keys
TOKEN = 'token'                    # CSRF token field name
CAS_SUCCESS = 'Login successful'   # CAS server successful login flag (find string in html page)
AUTH = {'username' : '',           # user field name
        'password' : '',           # password field name
        'submit' : 'Login'         # login submit button
       }
SCRIPT = 'manage.py shell --plain < get_pgt.py' # A script to extract the PGT from your proxying server

#Cribbed from django-treebeard
def get_db_conf():
    conf, options = {}, {}
    for name in ('ENGINE', 'NAME', 'USER', 'PASSWORD', 'HOST', 'PORT'):
        conf[name] = os.environ.get('DATABASE_' + name, '')
    engine = conf['ENGINE']
    if engine == '':
        engine = 'sqlite3'
    elif engine in ('postgres', 'postgresql', 'psycopg2'):
        engine = 'postgresql_psycopg2'
    if '.' not in engine:
        engine = 'django.db.backends.' + engine
    conf['ENGINE'] = engine

    if engine == 'django.db.backends.sqlite3':
        conf['TEST_NAME'] = conf['NAME'] = ':memory:'
    elif engine in ('django.db.backends.mysql',
                    'django.db.backends.postgresql_psycopg2'):
        if not conf['NAME']:
            conf['NAME'] = 'cas'
        # randomizing the test db name, so we can safely run multiple tests at
        # the same time
        conf['TEST_NAME'] = "test_%s_%s" % (conf['NAME'],
            ''.join(random.choice(string.letters) for _ in range(15)))
        if conf['USER'] == '':
            conf['USER'] = {
                'django.db.backends.mysql': 'root',
                'django.db.backends.postgresql_psycopg2': 'postgres'}[engine]
        if engine == 'django.db.backends.mysql':
            conf['OPTIONS'] = {
               'init_command': 'SET storage_engine=INNODB,'
                               'character_set_connection=utf8,'
                               'collation_connection=utf8_unicode_ci'}
    return conf

DATABASES = {'default': get_db_conf()}
SECRET_KEY = 'cascascas'
