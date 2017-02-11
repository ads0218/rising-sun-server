from datetime import timedelta
from celery.schedules import crontab


class CeleryConfig(object):
    """
        celery beat is a scheduler. It kicks off tasks at regular intervals,
        which are then executed by the worker nodes available in the cluster.
        crontab : If you want more control over when the task is executed,
        for example, a particular time of day or day of the week,
        you can use the crontab schedule type

    """

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']

    CELERYBEAT_SCHEDULE = {
        'byerook_crawl': {
            'task': 'app_server.tasks.celerybeat.byerook_crawl.crawl_byerook',
            'schedule': timedelta(minutes=5) #crontab(minute=0, hour='*')
        },

        'gyocharo_crawl': {
            'task': 'app_server.tasks.celerybeat.gyocharo_crawl.crawl_gyocharo',
            'schedule': timedelta(minutes=5) #crontab(minute=0, hour='*')
        },
        'naver_crawl': {
            'task': 'app_server.tasks.celerybeat.naver_crawl.crawl_naver',
            'schedule': timedelta(minutes=5)  # crontab(minute=0, hour='*')
        }
    }
