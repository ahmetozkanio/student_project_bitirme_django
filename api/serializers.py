
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from lessons.models import Attendance, Lesson, Message
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
class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

