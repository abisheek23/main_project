from django.shortcuts import render

# Create your views here.

def log(req):
    return render(req,'login.html')