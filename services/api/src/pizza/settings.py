import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIXTURE_DIRS = (os.path.join(BASE_DIR, 'fixtures'), )

SECRET_KEY = '&4kpf2d=)cxh=vojs)$pq&k38ggtcvu*(odwr2k-&p)!3=&f0b'

DEBUG = True


ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'pizza',
]

STATIC_URL = '/static/'

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'pizza.urls'

WSGI_APPLICATION = 'pizza.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_USER'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': 5432
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'PAGINATE_BY': 100
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [],
        },
    },
]

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
}
