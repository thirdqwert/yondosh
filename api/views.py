from rest_framework import views, generics, mixins, permissions
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
from .models import Habit, HabitLog, Task, News, UserProfile, Note, Spending, TargetMoney
from .utils import IsAnonymous

class RegisterAPIView(views.APIView):
    permission_classes = [IsAnonymous]
    def post(self, request):
        # post_telegramId = request.data.get('telegramId')

        # if post_telegramId:
        #     is_user = User.objects.filter(telegramId=post_telegramId).exists()

        #     if is_user:
        #         user = User.objects.get(telegramId=post_telegramId)
        #         serializer = RegisterSerializer(user, context={'request': request})
        #         refresh = RefreshToken.for_user(user)
        #         access = str(refresh.access_token)
        #         return Response({**serializer.data, **{"access": access, "refresh": str(refresh)}})

        serializer = RegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserProfileAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = generics.get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(queryset, context={'request': request})
        return Response(serializer.data)


class TelegramConn(generics.CreateAPIView):
    serializer_class = TelegramDeviceSerializer



class HabitMix(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
    ):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        set = Habit.objects.filter(active=True, startTime__hour=19, startTime__minute=29)
        print(set)
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        return Habit.objects.filter(habitUser=self.request.user)


class HabitLogListCreate(generics.ListCreateAPIView):
    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitLog.objects.filter(habitUser=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(habitUser=self.request.user)
    

class TaskMix(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
    ):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(taskUser=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(taskUser=self.request.user)


class NewsMix(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
):
    queryset = News.objects.filter(is_allowed=True)
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        
    def perform_create(self, serializer):
        serializer.save(newsUser=self.request.user)


class NoteAPIView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class SpendingAPIView(generics.ListCreateAPIView):
    serializer_class = SpendingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Spending.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TargetMoneyMix(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = TargetMoneySerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def get_queryset(self):
        return TargetMoney.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
