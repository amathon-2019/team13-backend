DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'channels',
]

PROJECT_APPS = [
    'apps.user',
    'apps.history',
]

INSTALLED_APPS = THIRD_PARTY_APPS + PROJECT_APPS + DJANGO_APPS
