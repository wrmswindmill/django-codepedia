"""
Django settings for CodePedia project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
# import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ieb3izb-*39(9(dlptwqs9c53no&vkb!=n8xjdle!s61e3*x)f'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
DATEBASE_NAME = 'code_pedia'


ALLOWED_HOSTS = ['*']

ADMINS=(
    ('Admin', 'alexkie@yeah.net')
)
MANAGERS = (
    ('Admin', 'alexkie@yeah.net')
)


AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',

)
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'xadmin',
    'crispy_forms',
    'captcha',
    'pure_pagination',  # 用于分页的库
    'taggit',
    'projects',
    'operations',
    'qa',
    'gunicorn',
    'djcelery',
     'kombu.transport.django',
    'django_extensions',
    # 'debug_toolbar',

]

AUTH_USER_MODEL = 'users.UserProfile'

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'CodePedia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # 用于将MEDIA_URL注册到HTML中,本例用于显示图片
                'CodePedia.context_processor.settings',
                'CodePedia.context_processor.get_web_stat',
                'CodePedia.context_processor.get_hot_projects',
                'CodePedia.context_processor.ip_address',
                'CodePedia.context_processor.settings',
                'django.template.context_processors.request',
            ],
        },
    },
]



WSGI_APPLICATION = 'CodePedia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'code_pedia',
        'USER': 'root',
        'PASSWORD': '111111',
        'HOST': '127.0.0.1',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',

    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False





# 配置邮件发送
EMAIL_HOST = 'smtp.yeah.net'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'alexkie@yeah.net'
EMAIL_HOST_PASSWORD = 'Mr8023Mr'
EMAIL_USE_TLS = False
EMAIL_FROM = 'alexkie@yeah.net'

#配置用户上传图片
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
#配置静态文件
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "production_static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    MEDIA_ROOT,
)

#配置Celery异步执行任务
###配置Broker
BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_TRANSPORT = 'redis'

APPEND_SLASH = True
#
#
#
import djcelery
djcelery. setup_loader()
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# debug_toolbar
# INTERNAL_IPS = ('127.0.0.1',)