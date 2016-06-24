"""
Django settings for fixit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS =[os.path.join(BASE_DIR, 'templates')]
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)
DOMAIN_PREFIX  =  "127.0.0.1:8080"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + [
    "django.core.context_processors.request"
]

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '-9eb1^u@xp==_@l4_(1#-euj*htfgs!r2jjv@eaq&i11dah8qq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fixitMain',
    'fixitAdmin',
    'fixitCustomers',
    'fixitTradesmen',
    'pycountry',
    'debug_toolbar',
            
    
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fixit.urls'

WSGI_APPLICATION = 'fixit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
##        'ENGINE': 'django.db.backends.sqlite3',
##        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        'ENGINE':                 'django.db.backends.sqlite3',
        'NAME':                    'fixitdb',
##        'USER':                      'james',
##        'PASSWORD':         '19hyper86',
##        'ROOT':                    '127.0.0.1',
##        'PORT':                    3306,
       
        
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'notifications@ndoozi.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
#This did the trick
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT          =           '/'
STATIC_URL           =           '/static/'
MEDIA_ROOT           =           'media'
MEDIA_URL            =          '/media/'

LOGIN_URL =  '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'