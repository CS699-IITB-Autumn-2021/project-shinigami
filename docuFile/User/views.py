from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from login.models import CertiInfo
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
@login_required(login_url = '/login')
def index(request):
    user = CertiInfo.objects.filter(user = request.session["username"])
    context = {
        'user': user
    }
    return render(request, 'User/index.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('http://localhost:8000')