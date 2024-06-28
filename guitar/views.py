from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # index page contains link to about
    return HttpResponse("Welcome! This is the index page! \nTo go to about page click <a href='/guitar/about/'>here</a>")

def about(request):
    # about page contains link back to index
    return HttpResponse("This is the about page. To return to index page please click <a href='/guitar/'>here</a>")


## ON PAGE 56 ###################