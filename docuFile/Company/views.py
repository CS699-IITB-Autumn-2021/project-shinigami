from django.shortcuts import render
from login.models import CertiInfo
from django.contrib.auth.models import User

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

def issue(request):
    if request.method == 'POST':
        username = request.POST.get('pid')
        print(username)
        user = User.objects.get(username = username)
        if user != None:
            typeC = request.POST.get('type')
            image = request.FILES['certificate']
            userC = CertiInfo.objects.create(user=username, type=typeC, certi=image)
            userC.save() 
    return render(request, 'Company/issue.html')
