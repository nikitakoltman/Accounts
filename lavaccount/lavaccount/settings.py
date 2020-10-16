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
    'rest_framework',
    # 'rest_framework.authtoken',
    # 'djoser',

    'home.apps.HomeConfig',
    'api.apps.ApiConfig',
    'support.apps.SupportConfig'
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 2

# Почта поддержки
SUPPORT_EMAIL = config.SUPPORT_EMAIL

STATIC_VERSION = 1
STATIC_VERSIONS = {
    'bootstrap-tour.min.css': 1,
    'bootstrap.min.css': 1,
    'sweet-alert.min.css': 1,

    'lk.css': 1,
    'style.css': 1,
    'support.css': 1,
    'table-theme-blue.css': 1,

    'bootstrap-tour.min.js': 1,
    'bootstrap.min.js': 1,
    'crypto-js.min.js': 1,
    'jquery-3.5.1.min.js': 1,
    'jquery.easing.min.js': 1,
    'jquery.tablesorter.min.js': 1,
    'PassGenJS.min.js': 1,
    'sweet-alert.min.js': 1,

    'ajax_setup.js': 1,
    'base.js': 1,
    'bubbly_animation.js': 1,
    'client_detection.js': 1,
    'email_change_form.js': 1,
    'form_message_handler.js': 1,
    'home.js': 1,
    'landing.js': 1,
    'lk.js': 1,
    'login.js': 1,
    'password_field_validation.js': 1,
    'register.js': 1,
    'tour.js': 1,

    'browserconfig.xml': 1,
    'manifest.json': 1
}
SITE_PROTOCOL = 'https'

SESSION_COOKIE_SAMESITE = 'Strict' # 'Lax'

# Защита XSS для старых браузеров
SECURE_BROWSER_XSS_FILTER = True

# TODO: раскомментировать параметры на продакшене

# Отказывать подключение к доменному имени через небезопасное
# соединение, в течение определенного периода времени (В секундах)
###SECURE_HSTS_SECONDS = 30 # Час 3600 # Год 31536000
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
