from django import forms
from .models import Announcement, Attendance, Message


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        # formda goruntulenecek alanlar
        fields = ["date","date2"]

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["lesson","title","description"]