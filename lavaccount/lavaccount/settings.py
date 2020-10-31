import os

from configs import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config.DJANGO_SECRET_KEY
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'crispy_forms',
    #'rest_framework',
    # 'rest_framework.authtoken',
    # 'djoser',

    'home.apps.HomeConfig',
    'api.apps.ApiConfig',
    'support.apps.SupportConfig'
]

###SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
###SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SAMESITE = 'Strict' # 'Lax'

# Защита XSS для старых браузеров
SECURE_BROWSER_XSS_FILTER = True

# Отказывать подключение к доменному имени через небезопасное
# соединение, в течение определенного периода времени (В секундах)
###SECURE_HSTS_SECONDS = 63072000 # 2 Года 63072000 # Час 3600 # Год 31536000
# Защита поддоменов
###SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Добавить сайт в список предварительной загрузки браузера
###SECURE_HSTS_PRELOAD = True

# Cookie будут отправляться только через HTTPS,
# что защитит от перехвата не незашифрованный файл cookie
###SESSION_COOKIE_SECURE = True

# CSRF cookie будут отправляться только через HTTPS,
# что защитит от перехвата не незашифрованный файл CSRF cookie
###CSRF_COOKIE_SECURE = True

# Если True, перенаправляет все запросы, отличные от HTTPS, на HTTPS
###SECURE_SSL_REDIRECT = True

# Защита Content-Security-Policy для контента
CSP_DEFAULT_SRC = ("'none'",)
CSP_STYLE_SRC = ("'self'",) # "'unsafe-inline'",
CSP_SCRIPT_SRC = ("'self'",)
CSP_FONT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'",)

## unsafe-inline разрешает встроенный CSS, например <h1 style = "margin-left: 30px;">
## Эта политика содержит 'unsafe-inline', что опасно в директиве style-src.


# Защита Referrer-Policy для контента
PERMISSIONS_POLICY = {
    'autoplay': ['none',],
    'camera': ['none',],
    'microphone': ['none',],
    'geolocation': ['none',],
    'display-capture': ['none',],
    'payment': ['none',],
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 3

# Почта поддержки
SUPPORT_EMAIL = config.SUPPORT_EMAIL

STATIC_VERSION = 1
SITE_PROTOCOL = 'https'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lavaccount.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lavaccount.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

EMAIL_USE_TLS = config.EMAIL_USE_TLS
EMAIL_HOST = config.EMAIL_HOST
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
EMAIL_PORT = config.EMAIL_PORT

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Для тестов в консоль

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticatedOrReadOnly',
#     ),
# }

# DJOSER = {
#     'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
#     'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
#     'ACTIVATION_URL': '#/activate/{uid}/{token}',
#     'SEND_ACTIVATION_EMAIL': True,
#     'SERIALIZERS': {},
# }

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': True,

#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': config.DJANGO_SECRET_KEY,
#     'VERIFYING_KEY': None,
#     'AUDIENCE': None,
#     'ISSUER': None,

#     'AUTH_HEADER_TYPES': ('JWT',),
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',

#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',

#     'JTI_CLAIM': 'jti',

#     'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
#     'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
# }
