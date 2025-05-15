# from pathlib import Path
# import os

# BASE_DIR = Path(__file__).resolve().parent.parent

# # MEDIA configuration for handling media files
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SECRET_KEY = 'your-secret-key'
# # SECRET_KEY = 'abchjdhjfhkdkkldldkjklsdjklsdfasjskskskskfkjfkluhjhjkhjkhkdskhdkshkhsdkhksdhfkjhheiueiueioeo873887736392929393393du3893h922jn'
# # SESSION_COOKIE_SECURE = True
# # CSRF_COOKIE_SECURE = True


# DEBUG = True
# ALLOWED_HOSTS = ['mygreatshop.com', 'www.mygreatshop.com', 'localhost', '127.0.0.1']


# # SECURE_HSTS_SECONDS = 31536000  # 1 year
# # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# # SECURE_HSTS_PRELOAD = True

# # SECURE_SSL_REDIRECT = True


# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# SECURE_SSL_REDIRECT = False


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'shop',  # Ensure the shop app is listed here
    
# ]

# # MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# # ROOT_URLCONF = 'ecommerce_website.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / "templates"],  # Correct directory for global templates
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# # AUTH_USER_MODEL set to CustomUser in the shop app
# AUTH_USER_MODEL = 'shop.CustomUser'

# # WSGI_APPLICATION = 'ecommerce_website.wsgi.application'

# # Static files configuration
# STATIC_URL = '/static/'

# # The directory where static files will be collected when running 'collectstatic'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# # The directories to look for static files during development
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]

# # Email settings (update these with your real mail server details)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.yourmailserver.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@example.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# # Database configuration (SQLite in development)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # Password validation (default settings)
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'

# USE_I18N = True
# USE_TZ = True

# LOGOUT_REDIRECT_URL = '/'  # Redirect to home page after logout
# LOGIN_REDIRECT_URL = '/'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'
# template_path = 'shop/invoice_template.html'
















































from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# MEDIA configuration for handling media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECRET_KEY = 'your-secret-key'

DEBUG = True
# ALLOWED_HOSTS = ['mygreatshop.com', 'www.mygreatshop.com', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# Disabling SSL redirect
SECURE_SSL_REDIRECT = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# settings.py
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',  # Ensure the shop app is listed here
     'sslserver',
       'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Correct directory for global templates
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

# AUTH_USER_MODEL set to CustomUser in the shop app
AUTH_USER_MODEL = 'shop.CustomUser'

# Static files configuration
STATIC_URL = '/static/'

# The directory where static files will be collected when running 'collectstatic'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# The directories to look for static files during development
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
ROOT_URLCONF = 'ecommerce_website.urls'

# Email settings (update these with your real mail server details)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourmailserver.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Database configuration (SQLite in development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation (default settings)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

LOGOUT_REDIRECT_URL = '/'  # Redirect to home page after logout
LOGIN_REDIRECT_URL = '/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
template_path = 'shop/invoice_template.html'
