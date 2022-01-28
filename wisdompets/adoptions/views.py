from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('<div>Home View</div>')


def pet_detail(request,pet_id):
    return HttpResponse(f'<div>pet_detail view with id {pet_id}</div>')
