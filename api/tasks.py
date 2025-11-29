import requests
import os
import requests
from celery import shared_task
from django.utils import timezone
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")


@shared_task(rate_limit='20/s')
def send_telegram_message(telegram_id, text):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    response = requests.post(url, data={'chat_id': telegram_id, 'text': text})
    print(response.json())


@shared_task(name="check_habits")
def check_habits():
    from .models import Habit, UserProfile
    print(1111)
    now = timezone.localtime()
    today = now.date()
    habits = Habit.objects.filter(active=True, startTime__hour=now.hour, startTime__minute=now.minute)
    for habit in habits:
        if habit.startHabitDate <= today < habit.endHabitDate:
            user_profile = UserProfile.objects.get(user=habit.habitUser)
            telegram_id = user_profile.telegram_device.telegramId
            if telegram_id is not None:
                print(telegram_id)
                text = f'"{habit.name}" odat vaqti boshlandi'
                send_telegram_message.delay(telegram_id, text)
            else:
                continue
        else:
            habit.active = False
            habit.save()
