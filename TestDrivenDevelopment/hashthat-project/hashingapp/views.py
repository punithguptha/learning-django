from django.shortcuts import render,redirect
from .forms import HashForm
import hashlib
from .models import HashModel
import pdb

# Create your views here.

def home(request):
    if request.method=="POST":
        # Below we are sending the data to the HashForm(Basically request.POST contains the data)
        filled_form=HashForm(request.POST)
        if filled_form.is_valid():
            text=filled_form.cleaned_data['text']
            current_hashed_text=hashlib.sha256(text.encode('utf-8')).hexdigest()
            try:
                HashModel.objects.get(hashed_text=current_hashed_text)
            except HashModel.DoesNotExist:
                hashModel=HashModel()
                hashModel.text=text
                hashModel.hashed_text=current_hashed_text
                hashModel.save()
            return redirect('hashview',id=current_hashed_text)
    form = HashForm()
    return render(request,'hashingapp/home.html',{'form':form})

def hashview(request,id):
    hash_model_entry=None
    try:
        hash_model_entry=HashModel.objects.get(hashed_text=id)
    except HashModel.DoesNotExist:
        print("Inside doesnot exist")
        hash_model_entry={
            'message':"Url doesnot exist",
        }
    return render(request,'hashingapp/hashPage.html',{'hash_data':hash_model_entry})
