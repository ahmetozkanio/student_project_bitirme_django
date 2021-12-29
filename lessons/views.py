from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import lessons
from lessons.models import Announcement, Attendance, Lesson, Message
from django.contrib.auth.models import User
from lessons.forms import AnnouncementForm, AttendanceForm, MessageForm
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
    attendance_form = AttendanceForm(request.POST or None)
    message_form = MessageForm(request.POST or None)
    message_text = Message.objects.all().filter(lesson = lesson_id)


    if message_form.is_valid():
        message = message_form.save(commit=False)
        message.lesson = lesson
        message.user = request.user
        message.save()



    if attendance_form.is_valid():

        attendance = attendance_form.save(commit=False)
        attendance.lesson = lesson
        attendance.save()
        attendance.qr_url =str(ALLOWED_HOSTS[1])+"/accounts/lesson/"+str(lesson_id)+"/attendance/"+str(attendance.id) + "/login/"
        attendance.save()
        messages.success(request,"Yoklama Olusturuldu") 


    if request.user.is_authenticated:
        lesson_join = current_user.lesson_joined.all()
    else:
        lesson_join = lessons
    context = {
        'lesson':lesson,
        'lesson_join':lesson_join,
        'attendances':attendances,
        'attendance_form':attendance_form,
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
    user = lesson.students.get(id = user_id)
    attendance.user_joined.add(user)
    

    
    messages.success(request,"Ders :" +lesson.name+" yoklamaniz alindi.") 
    return redirect("index")



def attendance_list(request):
    current_user = request.user
    attendances = Attendance.objects.all().order_by('-date_now')
    if request.user.is_authenticated:
        joined = current_user.attendance_joined.all()
    else:
        joined = attendances
    context = {
        'attendances':attendances,
        'lesson_join' :joined,
    }
    return render(request,'attendances/attendances.html',context)


def attendance_detail(request,attendance_id):
    current_user = request.user
    attendance = Attendance.objects.get(id = attendance_id)
    context = {
        'attendance':attendance
    }
    return render(request,'attendances/attendance.html',context)


def attendance_remove(request):
    lesson = Lesson.objects.get(id = request.POST['lesson_id'])#lesson.html
    attendance = Attendance.objects.get(lesson = lesson)
    attendance(avaliable = False)
    return redirect('lessons/lesson.html')


def announcement_add(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Duyuru Basariyla Olusturuldu.")
            return redirect('announcements')
        else :
            messages.success(request,"Duyuru Olusturulamadi.")
    else:
        form = AnnouncementForm()        
    return render(request,'announcements/announcement-add.html',{'announ_form':form})

def announcement_list(request):
    current_user = request.user
    announcements = Announcement.objects.all().order_by('-date')
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
    announcement = get_object_or_404(Announcement, id=announcement_id)
    form = AnnouncementForm(request.POST or None, instance=announcement)
    if form.is_valid():
        announcement = form.save(commit=False)
        # hangi kullanici giris yapmissa duyuru ona gore eklenecek
        announcement.author = request.user
        # aslinda kayit bu satirdan sonra oluyor cunku ustteki save() commit=false yaptik bilerek
        announcement.save()
        messages.success(request, "Duyuru basariyla guncellendi")
        return redirect("announcements")
    return render(request, "announcements/update-announcement.html", {"form": form})

def announcement_delete(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.delete()
    messages.success(request, "Duyuru basariyla silindi.")
    return redirect("announcements")


def qr_site(request,attendance_id):
    



    name = "Hosgeldin Yoklaman Alinmistir..."
    obj = Attendance.objects.get(id = attendance_id )
    context = {
        'name' :name,
        'obj':obj
    }
    return render(request,'attendances/qr_code.html',context)