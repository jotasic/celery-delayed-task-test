import logging

from celery import current_task, shared_task

logger = logging.getLogger()


@shared_task
def run_task(name):
    logger.info(f"[{current_task.request.hostname}-{current_task.request.id}]  SUCCESS NAME: {name}")
