
from django.contrib.auth.models import User
from django.db.models.base import Model
from rest_framework.serializers import ModelSerializer
from lessons.models import Attendance, Lesson, Message
from events.models import Event
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'



class LessonSerializer(ModelSerializer):

    students = UserSerializer(many=True)
    class Meta:
        model = Lesson
        fields = '__all__'

class AttendanceSerializer(ModelSerializer):
   
    lesson = LessonSerializer(many=False)
    user_joined = UserSerializer(many=True)
    class Meta:
        model = Attendance
        fields = ['id', 'lesson', 'user_joined', 'date', 'date2', 'avaliable']


class MessagesSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Message
        fields = '__all__'
        
class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        
class EventSerializer(ModelSerializer):
    teacher = UserSerializer(many=False)
    students = UserSerializer(many=True)
   
    class Meta:
        model = Event
        fields = '__all__'