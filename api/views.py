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
from .serializers import AttendanceSerializer, EventSerializer, LessonSerializer, MessageSerializer, MessagesSerializer, UserSerializer
from lessons.models import Lesson, Attendance, Message

from api import serializers



#USER ##################################

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many= True)
    return Response(serializer.data)




#USER ##################################


#EVENT######################

class EventList(APIView):

    def get(self,request,format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events,many= True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#EVENT######################


class LessonList(APIView):


    def get(self,request,format=None):
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons,many= True)
        return Response(serializer.data)

    
    def post(self,request,format=None):
        data = request.data

        lesson = Lesson.objects.create(
            teacher = data['teacher'],
            name = data['name'],
            description = data['description'] 
        )
        serializer = LessonSerializer(lesson, many=False)
        return Response(serializer.data)

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
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET'])
# def getAttendances(request):
#     attendances = Attendance.objects.all()
#     serializer = AttendanceSerializer(attendances,many= True)
#     return Response(serializer.data)



class MessageList(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self,request,format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
    
    
# @api_view(['GET'])
# def getMessages(request):
    
#     messages = Message.objects.all()
#     serializer = MessageSerializer(messages,many= True)
#     return Response(serializer.data)

    # def get(self,request,lesson_id,format=None):
        
    #     messages = Message.objects.filter(lesson__id =lesson_id)
    #     serializer = MessageSerializer(messages,many= True)
    #     return Response(serializer.data)