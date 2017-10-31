import multiprocessing

bind = '127.0.0.1:8000'
workers = 2
errorlog = '/home/pdl/ak/django-codepedia/gunicorn.error.log'
proc_name = 'gunicorn_codepedia'