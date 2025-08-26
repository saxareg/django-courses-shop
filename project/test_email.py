from django.conf import settings
from django.core.mail import send_mail
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'твой_проект.settings')
django.setup()


send_mail(
    'Тест из магазина курсов 🎓',
    'Ура! Почта работает!',
    settings.DEFAULT_FROM_EMAIL,
    ['courseshop12321@gmail.com'],
)
print("Письмо отправлено! Проверь почту.")
