from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = '/login')
def index(request):
    return render(request, 'User/index.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')