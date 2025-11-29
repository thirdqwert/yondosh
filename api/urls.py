from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .swagger_settings import urlpatterns as url_swagger
from . import views

paths = [
    # польхователь
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.UserProfileAPIView.as_view(), name='user_profile'),
    # подключение
    path('connect/telegram/', views.TelegramConnAPIView.as_view(), name='telegram_connect'),
    # привычки
    path('habits/', views.HabitListCreateAPIView.as_view(), name='habits'),
    path('habits/<int:pk>/', views.HabitRetrieveDestroyAPIView.as_view(), name='habit_detail'),
    path('habit/status/', views.HabitLogListCreate.as_view(), name='habit_status'),
    # задачи
    path('tasks/', views.TaskListCreateAPIView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskRetrieveDestroyAPIView.as_view(), name='task_detail'),
    # новости
    path('news/', views.NewsListCreateAPIView.as_view(), name='news'),
    path('news/<int:pk>/', views.NewsRetrieveDestroyAPIView.as_view(), name='news_detail'),
    # заметки
    path('notes/', views.NoteAPIView.as_view(), name='notes'),
    # финансы
    path('finances/spendings/', views.SpendingAPIView.as_view(), name='spendings'),
    path('finances/targets/', views.TargetListCreateAPIView.as_view(), name='targets'),
    path('finances/targets/<int:pk>/', views.TargetUpdateAPIView.as_view(), name='targets_detail'),
]

urlpatterns = paths + url_swagger
