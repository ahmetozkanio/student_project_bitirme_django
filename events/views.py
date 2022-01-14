from asyncio import events
from django.shortcuts import render,redirect
from events.forms import EventForm
from django.contrib import messages
from django.contrib.auth.models import User
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



def event_create(request):
    current_user = request.user
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            
            event =form.save(commit=False)
            event.teacher = current_user
            event.save()
                  
            messages.success(request,"Etkinlik Basariyla Olusturuldu.")
            return redirect('events')
        else :
            messages.success(request,"Etkinlik Olusturulamadi.")
    else:
        form = EventForm()        
    return render(request,'events/event_add.html',{'event_form':form})


def event_detail(request,event_id):
    pass
    current_user = request.user

    event = Event.objects.get(id = event_id)
 

    context = {
       'event':event
    }

    return render(request,'events/event.html',context)

def event_join(request):
    event_id = request.POST['event_id']
    user_id = request.POST['user_id']
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id = user_id)
    messages.success(request,"Etkinlige Kayit Oldunuz.") 
    event.students.add(user)
    return redirect('events')