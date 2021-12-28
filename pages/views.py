from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['courses'] = Course.objects.filter(avaliable=True).order_by('-date')[:2]
        # context['total_course'] = Course.objects.filter(avaliable=True).count() 
        # context['total_students'] = User.objects.filter().count() 
        # context['total_teachers'] = Teacher.objects.filter().count() 

        return context