from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
import pytz

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'user', 'type', 'first_name', 'last_name', 'email', 'photo']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'description', 'teacher', 'students']

class MaterialSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = ['id', 'course', 'file', 'filename']

    def get_filename(self, obj):
        filename = obj.file.name.split('/')[-1].replace('%20', ' ')
        return filename

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'student', 'course', 'description']

class StatusSerializer(serializers.ModelSerializer):
    formatted_timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Status
        fields = ['id', 'student', 'timestamp', 'description', 'formatted_timestamp']

    def get_formatted_timestamp(self, obj):
        timestamp = obj.timestamp.astimezone(pytz.timezone('Asia/Singapore'))
        formatted_timestamp = timestamp.strftime('%d %b %Y, %I:%M %p')
        return formatted_timestamp

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'room_name', 'admin', 'members', 'chat_log']

class EnrolNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolNotification
        fields = ['id', 'course', 'student', 'teacher', 'read']

class MaterialNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialNotification
        fields = ['id', 'material', 'student', 'read']