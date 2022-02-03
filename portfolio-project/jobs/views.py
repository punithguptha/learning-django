from django.shortcuts import render

# Create your views here.

def home(request):
    # Django automatically refers content from the templates folder, so we dont need to mention it explicitly..So we are using jobs/sai.html to refer to the content
    return render(request,"jobs/home.html")
