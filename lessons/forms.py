
from tkinter.ttk import Style
from turtle import width
from django import forms

from .models import Announcement, Attendance, Lesson, LessonFiles, Message


class LessonFilesForm(forms.ModelForm):
    title = forms.CharField( label='Belge Basligi',widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Belge Basligi'
    }))
    file = forms.FileField( label='Dosya Sec',widget = forms.ClearableFileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Sec',
       
    }))
    avaliable = forms.BooleanField(initial=True,required=False, label='Yayinlansin')
    class Meta:
        model = LessonFiles
        fields = ["title","file",'avaliable']

class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        # formda goruntulenecek alanlar
        fields = ["date","date2","avaliable"]


class MessageForm(forms.ModelForm):
    text = forms.CharField(label=False,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Mesajiniz',
        'style':'min-width:200px;max-width:280px;max-height:37px;'
        
    }))
    class Meta:
        model = Message
        fields = ["text"]


class AnnouncementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
   
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        self.fields["lesson"].queryset = Lesson.objects.filter(teacher=user)
       
    lesson = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)

    class Meta:
        model = Announcement
        fields = ["lesson","title","description"]
class AnnouncementUpdateForm(forms.ModelForm):


    class Meta:
        model = Announcement
        fields = ["title","description"]

class LessonForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop("user")
    #     print(user)
    #     super(AnnouncementForm, self).__init__(*args, **kwargs)
    #     self.fields["lesson"].queryset = Lesson.objects.filter(teacher=user)
       
    # lesson = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)

    class Meta:
        model = Lesson
        fields = ["name","image","description"]

