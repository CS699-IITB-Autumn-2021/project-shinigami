from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect

@login_required(login_url = '/login')
def index(request):
    return render(request, 'Company/index.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('http://localhost:8000')