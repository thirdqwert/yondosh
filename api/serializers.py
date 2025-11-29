from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Habit, HabitLog, Task, News, UserProfile, TelegramDeviсe, Note, Spending, TargetMoney
from .utils import generate_unique_code


class RegisterSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # def generate_password(self, length=8):
    #     letters = string.ascii_letters + string.digits
    #     return ''.join(random.choice(letters) for _ in range(length))
         

    def validate(self, attrs):
        # telegramId = attrs.get('telegramId')
        # if telegramId:
        #     return attrs

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Parollar mos kelmayapti!')
        return super().validate(attrs)
    

    def create(self, validated_data):
        # telegramId = validated_data.get('telegramId')

        # if telegramId:
        #     validated_data['username'] = f'user_{telegramId}'
        #     user = User.objects.create_user(**validated_data)
        #     password = self.generate_password()
        #     user.set_password(password)
        #     return user
        

        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        key = generate_unique_code(UserProfile)
        UserProfile.objects.create(user=user, telegram_key=key)
        return user
    

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2'] # 'telegramId'


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    telegram_devices = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'telegram_key', 'telegram_devices']

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
        }

    def get_telegram_devices(self, obj):
        devices = obj.telegram_devices.all()
        data = [
            {
                "id": device.id,
                "telegramId": device.telegramId
            } for device in devices
        ]
        return data

class TelegramDeviceSerializer(serializers.ModelSerializer):
    key = serializers.IntegerField(write_only=True)

    def validate(self, data):
        is_exist = UserProfile.objects.filter(telegram_key=data['key']).exists()
        if not is_exist:
            raise serializers.ValidationError("Bunday kalit yo'q")
        
        return super().validate(data)
    
    def create(self, validated_data):
        user_profile = UserProfile.objects.get(telegram_key=validated_data['key'])
        telegram_id = validated_data['telegramId']
        telegram_device = TelegramDeviсe.objects.create(profile=user_profile, telegramId=telegram_id)
        user_profile.telegram_key = generate_unique_code(UserProfile)
        user_profile.save()
        return telegram_device
    
    class Meta:
        model = TelegramDeviсe
        fields = ['id', 'telegramId', 'key']


class HabitLogSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # user = self.request.user
        # habit = data['habit']
        # lastLog = HabitLog.objects.filter(habitUser=self.re)
        now = timezone.localtime()
        today = now.date()
        lastLog = data['habit'].habit_logs.last()
        if lastLog is not None and lastLog.date == today:
            raise serializers.ValidationError('Bu odat bugun qayd etilgan edi')
        
        return super().validate(data)
    
    class Meta:
        model = HabitLog
        fields = ['id', 'habitUser', 'habit', 'status', 'date']
        read_only_fields = ['habitUser', 'date']


class HabitSerializer(serializers.ModelSerializer):
    habit_logs = HabitLogSerializer(many=True, read_only=True)
    
    def create(self, validated_data):
        now = timezone.localtime()
        today = now.date()
        days_count = timedelta(days=validated_data['days'] + 1)
        validated_data['endHabitDate'] = today + days_count
        return super().create(validated_data)
    
    class Meta:
        model = Habit
        fields = ['id', 'habitUser', 'name', 'startTime', 'endTime','startHabitDate', 'endHabitDate', 'targetHabit', 'days', 'habit_logs']
        read_only_fields = ['startHabitDate', 'endHabitDate']


class TaskSerializer(serializers.ModelSerializer):

    def validate(self, data):
        now = timezone.localtime()
        today = now.date()
        if data['date'] < today:
            raise serializers.ValidationError("Bu sana o'tib ketgan")
        return super().validate(data)
    
    
    class Meta:
        model = Task
        fields = ['id', 'taskUser', 'name', 'date']
        read_only_fields = ['taskUser']


class NewsSerializer(serializers.ModelSerializer):
    habit_id = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),
        source='habit',
        write_only=True
    )

    habit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'newsUser', 'habit', 'habit_id', 'title', 'desc', 'is_allowed', 'created_at']
        read_only_fields = ['newsUser', 'habit', 'habit_id', 'is_allowed', 'created_at']


    def get_habit(self, obj):
        return {
            "id": obj.habit.id,
            "name": obj.habit.name,
            "startTime": obj.habit.startTime,
            "endTime": obj.habit.endTime,
            "targetHabit": obj.habit.targetHabit,
            "days": obj.habit.days
        }
    

class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'text', 'date']
        read_only_fields = ['user']


class SpendingSerializer(serializers.ModelSerializer):


    class Meta:
        model = Spending
        fields = ['id', 'user', 'amount','date', 'category', 'comment']
        read_only_fields = ['user']


class TargetMoneySerializer(serializers.ModelSerializer):

    class Meta:
        model = TargetMoney
        fields = ['id', 'user', 'text', 'target_amount', 'current_amount']