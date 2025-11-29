from django.contrib import admin
from .models import Habit, HabitLog, Task, News, UserProfile, TelegramDevice, Note, Spending, TargetMoney
admin.site.register(Habit)
admin.site.register(HabitLog)
admin.site.register(Task)
admin.site.register(News)
admin.site.register(UserProfile)
admin.site.register(TelegramDevice)
admin.site.register(Note)
admin.site.register(Spending)
admin.site.register(TargetMoney)