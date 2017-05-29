# Django settings for pybbm_org project.
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Pavel Zhukov', 'gelios@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_ENV_MYSQL_DATABASE', 'local_db'),
        'HOST': os.environ.get('DB_PORT_3306_TCP_ADDR', 'localhost'),
        'PORT': os.environ.get('DB_PORT_3306_TCP_PORT', 3306),
        'USER': 'root',
        'PASSWORD': os.environ.get('DB_ENV_MYSQL_ROOT_PASSWORD', 'pass'),
        'TEST_CHARSET': 'UTF8',
        'ATOMIC_REQUESTS': True,
    }
}

if 'MC_PORT_11211_TCP_ADDR' in os.environ and 'MC_PORT_11211_TCP_PORT' in os.environ:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '%s:%s' % (os.environ['MC_PORT_11211_TCP_ADDR'],
                                   os.environ['MC_PORT_11211_TCP_PORT']),
            'TIMEOUT': 186400,
            'KEY_PREFIX': 'pybbm_org'
        }
    }

ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = '/media/'

STATIC_ROOT = ''

STATIC_URL = '/media/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pybb.middleware.PybbMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    'pybbm_org.middleware.RemoteAddrMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'pybb.context_processors.processor',
    'account.context_processors.account'
)

ROOT_URLCONF = 'pybbm_org.urls'

WSGI_APPLICATION = 'pybbm_org.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'sorl.thumbnail',
    'pybb',
    'pybbm_org',
    'pytils',
    'pure_pagination',
    'account',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'captcha',
    'gunicorn',
    'boto',
    'storages'
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_REDIRECT_URL = '/profile/edit/'
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = False
CAPTCHA_FONT_PATH = 'fonts/captcha_font.ttf'
CAPTCHA_FONT_SIZE = 28
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_LENGTH = 5
CAPTCHA_LETTER_ROTATION = (-10, 15)
# CAPTCHA_TIMEOUT = 1
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_arcs',)

PYBB_ATTACHMENT_ENABLE = True
PYBB_TEMPLATE = 'site_base.html'

SECRET_KEY = 'test_key'

if 'REDIS_PORT_6379_TCP_ADDR' in os.environ and 'REDIS_PORT_6379_TCP_PORT' in os.environ:
    BROKER_URL = 'redis://%s:%s' % (os.environ['REDIS_PORT_6379_TCP_ADDR'],
                                    os.environ['REDIS_PORT_6379_TCP_PORT'])
else:
    BROKER_URL = 'django://'
CELERY_DEFAULT_QUEUE = 'pybbm_org_celery'

try:
    from settings_local import *
except ImportError:
    pass
