# from celery import Celery
# from app.config import REDIS_URL

# celery_app = Celery(
#     "deploy_tasks",
#     broker=REDIS_URL,
#     backend=REDIS_URL
# )

# celery_app.conf.task_routes = {
#     "app.tasks.deploy_repo": {"queue": "deployments"}
# }
# # import tasks so celery registers them
# import app.tasks
from celery import Celery
from app.config import REDIS_URL

celery_app = Celery(
    "deploy_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# automatically discover tasks
celery_app.autodiscover_tasks(["app"])