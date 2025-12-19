from celery import shared_task

@shared_task
def celery_test():
    return "Task executed successfully!"


@shared_task
def celery_periodic_task():
    return "Periodic task executed successfully!"



from django.core.mail import send_mail

@shared_task
def alert_send_mail(alert_message):
    send_mail(
        subject="⚠️ALARM⚠️",
        message=alert_message,
        from_email=None,  # uses DEFAULT_FROM_EMAIL
        recipient_list=["mehranrayati2003@gmail.com", "motamednia2003@gmail.com"],
        fail_silently=False,
    )
