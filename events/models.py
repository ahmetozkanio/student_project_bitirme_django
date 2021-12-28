from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.


class Event(models.Model):
    teacher = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=128,unique=True,verbose_name="Etkinlik adi")
    image  = models.ImageField(upload_to="events/%Y/%m/%d/",default = "events/default_lesson_image.png")
    title = models.CharField(max_length=128, null=True,verbose_name="Baslik")
    description = RichTextField(verbose_name="Icerik")
    students = models.ManyToManyField(User, blank=True,related_name='event_joined')
    
    date = models.DateTimeField(auto_now=True)
    avaliable = models.BooleanField(default =True)
    
    def __str__(self):
        return self.name