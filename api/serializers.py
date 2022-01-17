
from datetime import date
from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.base import Model
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer
from lessons.models import Announcement, Attendance, Lesson, Message
from events.models import Event
from rest_framework import serializers

##Register 
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name','is_staff')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff= validated_data['is_staff']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','username','password','first_name','last_name','email','is_staff','date_joined')

class UserProfileSerialize(ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','is_staff','date_joined')

class LessonAddSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

class LessonSerializer(ModelSerializer):
    students = UserSerializer(many=True)
    class Meta:
        model = Lesson
        fields = '__all__'

class LessonJoinedStudentSerializer(ModelSerializer):

    students = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())
    name = serializers.CharField(required = False)
    
    class Meta:
        model = Lesson
        fields = '__all__'

class AttendanceStudentJoinSerializer(ModelSerializer):

    user_joined = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())
    lesson = serializers.CharField(required = False)
    date = serializers.CharField(required = False) 
    date2 = serializers.CharField(required = False) 

    class Meta:
        model = Attendance
        fields = '__all__'
        

class AttendanceSerializer(ModelSerializer):
   
    lesson = LessonSerializer(many=False)
    user_joined = UserSerializer(many=True)
    class Meta:
        model = Attendance
        fields = ['id', 'lesson', 'user_joined', 'date', 'date2', 'avaliable']

class AttendanceCreateSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'lesson', 'user_joined', 'date', 'date2', 'avaliable']


class MessagesSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Message
        fields = '__all__'
        
class MessageAddSerializer(ModelSerializer):
 
   
    class Meta:
        model = Message
        fields = ('lesson',"user","text")
        
class EventSerializer(ModelSerializer):
    teacher = UserSerializer(many=False)
    students = UserSerializer(many=True)
   
    class Meta:
        model = Event
        fields = '__all__'

class EventCreateSerializer(ModelSerializer):
   
    class Meta:
        model = Event
        fields = '__all__'






class LessonListSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
class AnnouncementSerializer(ModelSerializer):
    lesson = LessonListSerializer(many=False)
    class Meta:
        model = Announcement
        fields = '__all__'
class AnnouncementCreateSerializer(ModelSerializer):

    class Meta:
        model = Announcement
        fields = '__all__'