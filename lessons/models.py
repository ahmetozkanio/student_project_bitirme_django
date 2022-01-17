from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
#qr
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw



class Lesson(models.Model):
    
    teacher = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=128,unique=True)
    image  = models.ImageField(upload_to="lessons/%Y/%m/%d/",default = "lessons/default_lesson_image.png")
    description = models.TextField(blank=True,null=True)
    students = models.ManyToManyField(User, blank=True,related_name='lesson_joined')
    date = models.DateTimeField(auto_now=True)
    avaliable = models.BooleanField(default =True)
    
    def __str__(self):
        return self.name

class Attendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='attendance_lesson')
    user_joined= models.ManyToManyField(User,blank=True,related_name="attendance_joined")
    date = models.DateTimeField()
    date2 = models.DateTimeField()
    date_now = models.DateTimeField(auto_now=True,unique=True)
    avaliable = models.BooleanField(default=True)

    qr_code = models.ImageField(upload_to='qr_codes',blank=True)
    qr_url=models.URLField(blank=True,null=True)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.qr_url)
        canvas = Image.new('RGB',(400, 400), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.lesson}-yoklama-{self.id}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)
        canvas.close()
        super().save(*args, **kwargs)






class Announcement(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = RichTextField()
    date = models.DateTimeField(auto_now=True)
    avaliable = models.BooleanField(default =True)
    def __str__(self):
        return self.title

class Message(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=255,verbose_name="Mesajiniz")
    date = models.DateTimeField(auto_now=True)
    avaliable = models.BooleanField(default =True)
    def __str__(self):
        return self.user.username
    