from django.shortcuts import render

from .models import Event

# Create your views here.



def event_list(request):
    
    current_user = request.user
    events = Event.objects.all().order_by('-date')
    
    if request.user.is_authenticated:
        event_join = current_user.event_joined.all()
    else:
        event_join = events
    
    context = {
        'events':events,
        'event_join' :event_join
    }
    return render(request,'events/events.html',context)




def event_detail(request,lesson_id):
    pass
    # current_user = request.user
    # lessons = Lesson.objects.all().order_by('-date')
    # lesson = Lesson.objects.get(id = lesson_id)
    # attendances = Attendance.objects.all().filter(lesson = lesson_id, avaliable = True)
    # attendance_form = AttendanceForm(request.POST or None)

    # message_form = MessageForm(request.POST or None)
    # message_text = Message.objects.all().filter(lesson = lesson_id)

    # if message_form.is_valid():
    #     message = message_form.save(commit=False)
    #     message.lesson = lesson
    #     message.user = request.user
    #     message.save()


    # if attendance_form.is_valid():
    #     attendance = attendance_form.save(commit=False)
    #     # Hangi Kullanici Giris yapmissa
    #     attendance.lesson = lesson
        
    #     attendance.save()
    #     messages.success(request,"Yoklama Olusturuldu") 


    # if request.user.is_authenticated:
    #     lesson_join = current_user.lesson_joined.all()
    # else:
    #     lesson_join = lessons

    # context = {
    #     'lesson':lesson,
    #     'lesson_join':lesson_join,
    #     'attendances':attendances,
    #     'attendance_form':attendance_form,
    #     'message_form':message_form,
    #     'message_text':message_text,
    # }

    # return render(request,'lessons/lesson.html',context)
