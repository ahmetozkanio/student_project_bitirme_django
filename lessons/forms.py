
from types import TracebackType
from django import forms

from .models import Announcement, Attendance, Lesson, Message




class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        # formda goruntulenecek alanlar
        fields = ["date","date2","avaliable"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]


class AnnouncementForm(forms.ModelForm):

     
  
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        print(user)
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        self.fields["lesson"].queryset = Lesson.objects.filter(teacher=user)
       
    lesson = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)

    class Meta:
        model = Announcement
        fields = ["lesson","title","description"]