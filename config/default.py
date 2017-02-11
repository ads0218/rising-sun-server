import os
import json
import datetime


class Config(object):


    BASE_SERVER = 'http://localhost'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../risingsun.db'

    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True

    API_SERVER = BASE_SERVER + '/api'
    ONLINE_LAST_MINUTES = 5000
    SESSION_ALIVE_MINUTES = 60 * 24 * 30 * 60  # 60days
    SECRET_KEY = 'gi3mHUx8hcLoQrnqP1XOkSORrjxZVkST'

    # REDIS
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0

    # SOCKETIO
    SOCKETIO_REDIS_URL = 'redis://localhost:6379/0'

    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']

    # section divide quotient. for example 100 -> 101 is 1 section

    # THUMBNAIL size
    SIGNAGE_WEB_SIZE = 300, 256

