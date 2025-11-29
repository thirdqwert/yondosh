from django.db import models
from django.contrib.auth.models import User


# class User(AbstractUser):
#     telegramId = models.CharField(max_length=100, unique=True, null=True, blank=True)

#     # Добавил потому что был конфликт с User(тот который в django) из заа relatedName
#     groups = models.ManyToManyField(
#         Group,
#         related_name="custom_user_set",  # <- поменяли related_name
#         blank=True,
#         help_text="The groups this user belongs to.",
#         verbose_name="groups",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name="custom_user_permissions_set",  # <- поменяли related_name
#         blank=True,
#         help_text="Specific permissions for this user.",
#         verbose_name="user permissions",
#     )


#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'


class Habit(models.Model):
    habitUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь привычки')
    name = models.CharField(max_length=200, verbose_name='Название привычки')
    startTime = models.TimeField(verbose_name='Время начало привычки')
    endTime = models.TimeField(verbose_name='Время конца привычки')
    startHabitDate = models.DateField(auto_now_add=True, verbose_name='Дата создания привычки')
    endHabitDate = models.DateField(verbose_name='Дата окончания привычки')
    targetHabit = models.CharField(max_length=500, verbose_name='Цель привычки')
    days = models.IntegerField(verbose_name='Количество дней')
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'


class HabitLog(models.Model):
    habitUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь привычки')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='habit_logs', verbose_name='Привычка')
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    status = models.BooleanField(verbose_name='Статус')


class Task(models.Model):
    taskUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь задачи')
    name = models.CharField(max_length=200, verbose_name='Название задачи')
    date = models.DateField(verbose_name='Дата задачи')


class News(models.Model):
    newsUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Новость пользователя')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Привычка')
    title = models.CharField(max_length=200, verbose_name='Название новости')
    desc = models.TextField(max_length=1000, verbose_name='Описание привычки')
    is_allowed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь профиля')
    telegram_key = models.IntegerField(blank=True, unique=True, null=True, verbose_name='Ключ для связи телеграм')



class TelegramDevice(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='telegram_device', verbose_name='Профиль девайса')
    telegramId = models.BigIntegerField(unique=True, verbose_name='телеграм ID пользователя')


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь отчета')
    title = models.CharField(max_length=200, verbose_name='Название отчета')
    text = models.TextField(max_length=2000, verbose_name='Текст отчета')
    date = models.DateField()


class Spending(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь траты')
    amount = models.IntegerField(verbose_name='Сколько потрачено')
    date = models.DateField()
    category = models.CharField(max_length=100, verbose_name='Категория траты')
    comment = models.TextField(max_length=200, verbose_name='Комментарий от пользователя')


class TargetMoney(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь цели')
    text = models.CharField(max_length=200, verbose_name='Комментарий цели')
    target_amount = models.IntegerField(verbose_name='Целевая сумма')
    current_amount = models.IntegerField(default=0, verbose_name='Нынешняя сумма')