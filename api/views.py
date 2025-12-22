from rest_framework import views, generics, mixins, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import (RegisterSerializer, 
                          HabitSerializer, 
                          HabitLogSerializer, 
                          TaskSerializer, 
                          NewsSerializer, 
                          UserProfileSerializer, 
                          TelegramDeviceSerializer,
                          NoteSerializer,
                          SpendingSerializer,
                          TargetMoneySerializer
                        )
from .models import Habit, HabitLog, Task, News, UserProfile, Note, Spending, TargetMoney, TelegramDevice


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class UserProfileAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        queryset = generics.get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(queryset, context={'request': request})
        return Response(serializer.data)


class TelegramConnAPIView(generics.GenericAPIView):
    serializer_class = TelegramDeviceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        try:
            device = TelegramDevice.objects.get(profile__user=request.user)
            device.delete()
            return Response({"detail": "Удалено"}, status=status.HTTP_204_NO_CONTENT)
        except TelegramDevice.DoesNotExist:
            return Response({"detail": "Не найдено"}, status=status.HTTP_404_NOT_FOUND)
    

class HabitListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(habitUser=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(habitUser=self.request.user)
    

class HabitRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Habit.objects.none()
        return Habit.objects.filter(habitUser=self.request.user)
    
class HabitLogListCreate(generics.ListCreateAPIView):
    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitLog.objects.filter(habitUser=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(habitUser=self.request.user)
    

class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(taskUser=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(taskUser=self.request.user)


class TaskRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # нужно что бы swagger не выдовал ошибку
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        return Task.objects.filter(taskUser=self.request.user)


class NewsListCreateAPIView(generics.ListCreateAPIView):
    queryset = News.objects.filter(is_allowed=True)
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]
        
    def perform_create(self, serializer):
        serializer.save(newsUser=self.request.user)


class NewsRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = News.objects.filter(is_allowed=True)
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]


class NoteListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteDestroyAPIView(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class SpendingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SpendingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Spending.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TargetListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TargetMoneySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return TargetMoney.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TargetUpdateAPIView(generics.UpdateAPIView):
    serializer_class = TargetMoneySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # нужно что бы swagger не выдовал ошибку
        if getattr(self, 'swagger_fake_view', False):
            return TargetMoney.objects.none()
        return TargetMoney.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
