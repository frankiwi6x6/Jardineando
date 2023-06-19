from pathlib import Path
import os
import locale

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-w_-^c08pkanh)b&8%y#k_*#g8w@-18m0%(v_b-ccl0cntgjly_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "core",
    "staff",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    # Configuración de Crispy Forms
    'crispy_forms',
    'crispy_bootstrap5',
    # Configuración de Django-allauth
    'django.contrib.sites',
    'allauth.account',
    'allauth',
    'allauth.socialaccount',
    # Desinstalar django-extensions en producción (Facebook)
    'django_countries',
    'pytz',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware', # Django-allauth
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "jardineando_projecto.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = "jardineando_projecto.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-CL'
TIME_ZONE = 'America/Santiago'      # Universal Cordinated Time
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('es-CL', 'Spanish (Chile)'),
    # Other language entries...
]

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

SITE_ID = 1


LOGIN_REDIRECT_URL = '/'

LOCALE_PATHS = [
    BASE_DIR / 'core' / 'locale',
]


MEDIA_URL = 'core/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'core/media')

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "jardineandoweb"
EMAIL_HOST_PASSWORD = "pzmimksdzlcqfdwp"


STRIPE_PUBLIC_KEY = "pk_test_51NImmlEPgDiK7ypN9gZLzlmPjMOotuLZ2l04v55UOBksXKAEfAcGI72w91ghAYWSoer5VjxOtlNmsvCzH9DpPj7X00AnP3ePDH"
STRIPE_SECRET_KEY = "sk_test_51NImmlEPgDiK7ypNb0fjnLJ59G8cbqs55AQYD7grks7qM8PNxMaFRY2IHsiPGKQlrrDiJpYD4CdirD7nbAoZIJaP00BD7vYgBj"


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

