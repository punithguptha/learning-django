from django.shortcuts import render, get_object_or_404
from .models import Job

# Create your views here.

def home(request):
    jobs=Job.objects.all()
    # Django automatically refers content from the templates folder, so we dont need to mention it explicitly..So we are using jobs/sai.html to refer to the content
    return render(request,"jobs/home.html",{'jobs':jobs})

def detail(request, job_id):
    job_detail = get_object_or_404(Job, pk=job_id)
    return render(request,"jobs/job_info.html",{"job_detail":job_detail})
