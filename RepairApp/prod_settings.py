# SECURITY WARNING: don't run with debug turned on in production!
import os

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'repair_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWD', 'ybh123'),
        'HOST': os.getenv('DB_HOST', 'repair_db'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
