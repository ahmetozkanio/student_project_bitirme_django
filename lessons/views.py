from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.views import logout
from lessons.models import Announcement, Attendance, Lesson, Message
from django.contrib.auth.models import User
from lessons.forms import AnnouncementForm, AnnouncementUpdateForm, AttendanceForm, LessonForm, MessageForm
from student.settings import ALLOWED_HOSTS



# Create your views here.


def lesson_list(request):
    current_user = request.user
    lessons = Lesson.objects.all().order_by('-date')
    if request.user.is_authenticated:
        lesson_join = current_user.lesson_joined.all()
    else:
        lesson_join = lessons
    context = {
        'lessons':lessons,
        'lesson_join' :lesson_join
    }
    return render(request,'lessons/lessons.html',context)

@login_required(login_url='login')
def lesson_detail(request,lesson_id):
    current_user = request.user
    lessons = Lesson.objects.all().order_by('-date')
    lesson = Lesson.objects.get(id = lesson_id)
    attendances = Attendance.objects.all().filter(lesson = lesson_id, avaliable = True)
    att_remove_last = Attendance.objects.last()
    attendance_remove_avaliable_last= att_remove_last

    attendance_form = AttendanceForm(request.POST or None)
    
    message_form = MessageForm(request.POST or None)
    message_text = Message.objects.all().filter(lesson = lesson_id)
   
    

    if message_form.is_valid():
        message = message_form.save(commit=False)
        message.lesson = lesson
        message.user = request.user
        message.save()
        return HttpResponseRedirect(reverse("lesson_detail", kwargs={'lesson_id': lesson_id}))



    if attendance_form.is_valid():

        attendance = attendance_form.save(commit=False)
        attendance.lesson = lesson
        attendance.save()
        attendance.qr_url =str(ALLOWED_HOSTS[1])+"/accounts/lesson/"+str(lesson_id)+"/attendance/"+str(attendance.id) + "/login"
        attendance.save()
        messages.success(request,"Yoklama Olusturuldu") 
        return HttpResponseRedirect(reverse("lesson_detail", kwargs={'lesson_id': lesson_id}))

    
   



    if request.user.is_authenticated:
        lesson_join = current_user.lesson_joined.all()
    else:
        lesson_join = lessons
    context = {
        'lesson':lesson,
        'lesson_join':lesson_join,
        'attendances':attendances,
        'attendance_form':attendance_form,
        'attendance_remove_avaliable_last':attendance_remove_avaliable_last,
        'message_form':message_form,
        'message_text':message_text,
    }
    return render(request,'lessons/lesson.html',context)


def lesson_add(request):
    lesson_id = request.POST['lesson_id']
    user_id = request.POST['user_id']
    lesson  = Lesson.objects.get(id=lesson_id)
    user = User.objects.get(id = user_id)
    messages.success(request,"Derse Kayit Oldunuz.") 
    lesson.students.add(user)
    return redirect('dashboard')


def lesson_create(request):
    current_user = request.user
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            
            lesson=form.save(commit=False)
            lesson.teacher = current_user
            lesson.save()
            lesson.students.add(request.user)
            lesson.save()           
            messages.success(request,"Ders Basariyla Olusturuldu.")
            return redirect('dashboard')
        else :
            messages.success(request,"Ders Olusturulamadi.")
    else:
        form = LessonForm()        
    return render(request,'lessons/lesson_add.html',{'lesson_form':form})



def attendance_add(request,lesson_id,attendance_id):
    
    # if(attendance_id_url != None):
    #     attendance_id = request.POST['attendance_id']
    #     user_id = request.POST["user_id"]   
    # else:
    # attendance_id= attendance_id_url
    user_id = request.user.id
       
    #lesson_id = request.POST["lesson_id"]
    
    
    attendance = Attendance.objects.get(id=attendance_id)
    lesson = attendance.lesson
    try:
        user = lesson.students.get(id = user_id)
    except User.DoesNotExist:
        user = None

    if user != None:
        if attendance.avaliable:
            
            attendance.user_joined.add(user)
            messages.success(request,"Ders :" +lesson.name+" yoklamaniz alindi.") 
           
            return redirect("index")
            
        elif attendance.avaliable == False:
            messages.success(request,"Yoklama kapanmistir Katilamadiniz.")
           
            return redirect("index")
        
    messages.success(request,"Bu derse kayitli degilsiniz yoklama alinmadi.")

    return redirect("index")
    

    



def attendance_list(request):
    current_user = request.user
    lessons = current_user.lesson_joined.all()
    
    attendances = Attendance.objects.filter(lesson__in= lessons).order_by('-date_now') 

    #Ogrencinin kayit oldugu kurslar
    #manytomanyt related name = lesson_joined
  

    if request.user.is_authenticated:
        joined = current_user.attendance_joined.all()
    else:
        joined = attendances
    context = {
        'attendances':attendances,
        'lesson_join' :joined,
        'lessons':lessons
    }
    return render(request,'attendances/attendances.html',context)


def attendance_detail(request,attendance_id):
    current_user = request.user
    attendance = Attendance.objects.get(id = attendance_id)
    context = {
        'attendance':attendance
    }
    return render(request,'attendances/attendance.html',context)


def attendance_remove(request,attendance_id):

    attendance = Attendance.objects.get(id =attendance_id)
    attendance.avaliable =False
    attendance.save()
    return redirect('attendances')


def announcement_add(request):
  
    if request.method == 'POST':
        form = AnnouncementForm(request.POST,user =request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Duyuru Basariyla Olusturuldu.")
            return redirect('announcements')
        else :
            messages.success(request,"Duyuru Olusturulamadi.")
    else:
        form = AnnouncementForm(user=request.user)        
    return render(request,'announcements/announcement-add.html',{'announ_form':form})

def announcement_list(request):
    current_user = request.user
    lessons = current_user.lesson_joined.all()
    
    announcements = Announcement.objects.filter(lesson__in =lessons).order_by('-date')
    context = {
        'announcements':announcements,
    }
    return render(request,'announcements/announcements.html',context)

def announcement_detail(request,announcement_id):
    current_user = request.user
    announcement = Announcement.objects.get(id = announcement_id)
    context = {
        'announcement':announcement
    }
    return render(request,'announcements/announcement.html',context)



def announcement_update(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    form = AnnouncementUpdateForm(request.POST or None,instance =announcement)
    
    if form.is_valid():
        form.save()

   
        messages.success(request, "Duyuru basariyla guncellendi")
        return redirect("announcements")
    return render(request, "announcements/update-announcement.html", {"form": form,"announcement":announcement})

def announcement_delete(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.delete()
    messages.success(request, "Duyuru basariyla silindi.")
    return redirect("announcements")


def qr_site(request,attendance_id):
   
    obj = Attendance.objects.get(id = attendance_id )
    context = {
        
        'obj':obj
    }
    return render(request,'attendances/qr_code.html',context)