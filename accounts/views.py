from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render



from .forms import LoginForm, RegisterForm
from lessons.models import Attendance
# Create your views here.


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,
                                        password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request,user)
                    return redirect('index')

                else:
                    messages.info(request, 'Disabled Account')

            else:
                messages.info(request, 'Check Your Username and Password')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form':form})


def register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account has been created, You can Login')
            return redirect('login')

    else:
        form = RegisterForm()        
    return render(request,'accounts/register.html',{'form':form})



def logout(request):
    auth_logout(request)
    return redirect('index')


@login_required(login_url='login')
def user_dashboard(request):
    #hangi kullanici giris yapmissa
    current_user =request.user

    #Ogrencinin kayit oldugu kurslar
    #manytomanyt related name = lesson_joined
    lessons = current_user.lesson_joined.all()
    context = {
        'lessons':lessons
    }
    return render(request,'dashboard.html',context)



def attendance_joined(request,lesson_id,attendance_id):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,
                                        password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request,user)
                    user_id = user.id
                    # attendance_add(request,lesson_id,attendance_id)
                    return redirect('attendance_add' , lesson_id=lesson_id, attendance_id=attendance_id )

                else:
                    messages.info(request, 'Disabled Account')

            else:
                messages.info(request, 'Check Your Username and Password')

    else:
        form = LoginForm()

    return render(request, 'attendances/attendance_user_login.html', {'form':form,'lesson_id':lesson_id,'attendance_id':attendance_id})