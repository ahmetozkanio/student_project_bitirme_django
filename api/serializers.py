
from rest_framework.serializers import ModelSerializer
from lessons.models import Attendance, Lesson, Message

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class AttendanceSerializer(ModelSerializer):
    
    class Meta:
        model = Attendance
        fields = '__all__'
class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'