from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_purchase_email(user_id, course_title):
    try:
        user = User.objects.get(id=user_id)
        subject = f'Спасибо за покупку курса: {course_title}'
        message = f'Здравствуйте, {user.username}!Спасибо за покупку курса "{course_title}" в нашем магазине.'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return f'Email sent to {user.email}'
    except Exception as e:
        return f'Error: {str(e)}'
