from celery import shared_task

@shared_task
def celery_test():
    return "Task executed successfully!"


@shared_task
def celery_periodic_task():
    return "Periodic task executed successfully!"