from django.shortcuts import render
from .models import Job

# Create your views here.

def home(request):
    jobs=Job.objects.all()
    # Django automatically refers content from the templates folder, so we dont need to mention it explicitly..So we are using jobs/sai.html to refer to the content
    return render(request,"jobs/home.html",{'jobs':jobs})
