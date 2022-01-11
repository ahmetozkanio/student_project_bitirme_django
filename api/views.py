from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
import api
from events.models import Event
from .serializers import UserProfileSerialize, AnnouncementCreateSerializer, AnnouncementSerializer, AttendanceCreateSerializer, AttendanceSerializer, EventCreateSerializer, EventSerializer, LessonAddSerializer, LessonSerializer, MessageAddSerializer, MessagesSerializer, UserSerializer
from lessons.models import Announcement, Lesson, Attendance, Message

from api import serializers
from rest_framework.parsers import JSONParser 


#USER ##################################
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import RegisterSerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ()
    serializer_class = RegisterSerializer
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_staff': user.is_staff,

        })

        
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many= True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserProfile(request,id):
    users = User.objects.get(id = id)
    serializer = UserProfileSerialize(users,many= False)
    return Response(serializer.data)


#USER ##################################


#EVENT######################

class EventList(APIView):

    def get(self,request,format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events,many= True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#EVENT######################




@api_view(['GET'])
def getLessons(request):
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons,many= True)
    return Response(serializer.data)

@api_view(['POST'])
def postLesson(request):
    serializer = LessonAddSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonDetail(APIView):


   
    def get_object(self, id):
        
        try:
            return Lesson.objects.get(id=id)
        except Lesson.DoesNotExist:
            raise Http404
        
    def get(self,request,id,format=None):
        lesson = self.get_object(id)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    
    def put(self,request,id,format=None):
        lesson = self.get_object(id)
        serializer =LessonSerializer(lesson,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id,format=None):
        lesson = self.get_object(id)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['PUT'])
# def updateLesson(request, id):
#     data = request.data
#     lesson = Lesson.objects.get(id =id)
   

#     serializer = LessonSerializer(lesson, data = request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def deleteLesson(request,id):
#     lesson = Lesson.objects.get(id =id)
#     lesson.delete()
#     return Response("Ders silindi!")


class AttendanceList(APIView):

    def get(self,request,format=None):
        attendances = Attendance.objects.all()
        serializer = AttendanceSerializer(attendances,many= True)
        return Response(serializer.data)

    def post(self,request,fornat=None):
        serializer = AttendanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class AnnouncementList(APIView):

    def get(self,request,format=None):
        attendances = Announcement.objects.all()
        serializer = AnnouncementSerializer(attendances,many= True)
        return Response(serializer.data)

    def post(self,request,fornat=None):
        serializer = AnnouncementCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def getAttendances(request):
#     attendances = Attendance.objects.all()
#     serializer = AttendanceSerializer(attendances,many= True)
#     return Response(serializer.data)


@api_view(['POST'])
def postMessage(request):
    serializer = MessageAddSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class MessageDetail(APIView):

    def get_object(self, lesson_id):
        
        try:
            return Message.objects.filter(lesson__id=lesson_id)
        except Lesson.DoesNotExist:
            raise Http404
              
    def get(self,request,lesson_id,format=None):
        
        messages = self.get_object(lesson_id)
        serializer = MessagesSerializer(messages,many= True)
        return Response(serializer.data)
    