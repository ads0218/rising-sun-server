from app_server.tasks.celery_manager import CeleryManager

celery = CeleryManager(config='config.celeryconfig.CeleryConfig')

from app_server.tasks.celerybeat.naver_crawl import crawl_naver
from app_server.tasks.celerybeat.gyocharo_crawl import crawl_gyocharo
from app_server.tasks.celerybeat.byerook_crawl import crawl_byerook