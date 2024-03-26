from zanko.settings import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ob4(%5uvqf9swtqijrn68xm=+h^eg39k)*vpo@3p1%-yuy#2!a'


DEBUG = False

ALLOWED_HOSTS = ['zankoapp.herokuapp.com','newzanko.herokuapp.com', 'https://www.drsehid.ir']

#INSTALLED_APPS = []

SITE_ID = 2

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [
    BASE_DIR / "statics"
]