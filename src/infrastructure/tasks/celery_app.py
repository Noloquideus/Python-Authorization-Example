from celery import Celery
from src.config import settings

celery = Celery("celery", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", include=["src.infrastructure.tasks.tasks"])
