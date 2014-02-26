#-*- coding: utf-8 -*-
"""
Django settings for profiling project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#qg$9+aujad#$mbt980%t628u(dau%$!f=&t%425szifn-p59%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    #'debug_toolbar',
    'app',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #'debug_toolbar.middleware.DebugToolbarMiddleware',

)

ROOT_URLCONF = 'profiling.urls'

WSGI_APPLICATION = 'profiling.wsgi.application'


# Database

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'app',
    'USER': 'root',
    'PASSWORD': 'root',
    'HOST': 'localhost', # Or an IP Address that your DB is hosted on
    'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


"""
A quick copy/paste action you can drop into your `./manage.py shell` session so any
queries executed are displayed in the shell output.

If sqlparse is available it will use that to pretty print the SQL:
http://code.google.com/p/python-sqlparse/
"""
from django.db.backends import util
try:
    import sqlparse
except ImportError:
    sqlparse = None
    print('ERROOOOO')

class PrintQueryWrapper(util.CursorDebugWrapper):
    def execute(self, sql, params=()):
        try:
            return self.cursor.execute(sql, params)
        finally:
            raw_sql = self.db.ops.last_executed_query(self.cursor, sql, params)
            if sqlparse:
                print(sqlparse.format(raw_sql, reindent=True))
            else:
                print(raw_sql)
            print()

util.CursorDebugWrapper = PrintQueryWrapper


#  A configuração do PrintQueryWrapper, sobreescre esta
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         # 'verbose': {
#         #     'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         # },
#         'simple': {
#             'format': '%(module)s %(message)s',
#         },
#     },
#     'handlers': {
#         'console':{
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/home/raul/dev/works-py3/profiling.log',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

'''
Só para remover o Warning de TMZ do Console
'''
import warnings
warnings.filterwarnings(
        'error', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')