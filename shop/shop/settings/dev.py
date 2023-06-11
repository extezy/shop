from .base import *

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': APP_DIR / 'db.sqlite3',
    }
}

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'}
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}
)
