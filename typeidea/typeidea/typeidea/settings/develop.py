from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea',
        'PASSWORD':'jing19961219',
        'HOST':'172.18.29.177',
        'PORT':3306,
        'USER':'root',
    }
}

DEBUG = True