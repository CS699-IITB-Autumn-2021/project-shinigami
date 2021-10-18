from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from User.models import certiRequest
from login.models import CertiInfo
from Company.models import viewRequest
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
@login_required(login_url = '/login')
def index(request):
    user = CertiInfo.objects.filter(user = request.COOKIES["username"])
    context = {
        'user': user,
        'username': request.COOKIES["username"]
    }
    return render(request, 'User/index.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('http://localhost:8000')

def pending(request):
    if request.method == 'POST':
        data = request.POST
        count = 1
        for i in data.keys():
            if count == 2:
                n = i
            count += 1 
        dec = n.split('_')[0]
        first = n.split('_')[1]
        last = n.split('_')[2]
        if dec == 'accept':
            r = viewRequest.objects.get(ifirst = first, ilast = last, uid = request.COOKIES["username"])
            r.status = 'A'
            r.save()
        elif dec == 'reject':
            r = viewRequest.objects.get(ifirst = first, ilast = last, uid = request.COOKIES["username"])
            r.delete()
    req = viewRequest.objects.filter(status = 'NA', uid = request.COOKIES["username"])
    context = {
        'req': req
    }
    return render(request, 'User/pending.html', context)

def granted(request):
    if request.method == 'POST':
        data = request.POST
        count = 1
        for i in data.keys():
            if count == 2:
                n = i
            count += 1 
        dec = n.split('_')[0]
        first = n.split('_')[1]
        last = n.split('_')[2]
        if dec == 'temp':
            r = viewRequest.objects.get(ifirst = first, ilast = last, uid = request.COOKIES["username"])
            r.status = 'NA'
            r.save()
        elif dec == 'per':
            r = viewRequest.objects.get(ifirst = first, ilast = last, uid = request.COOKIES["username"])
            r.delete()      
    granted = viewRequest.objects.filter(status = 'A', uid = request.COOKIES["username"])
    context = {
        'grant': granted
    }
    return render(request, 'User/granted.html', context)

def request(request):
    if request.method == 'POST':
        insti = request.POST.get('iid')
        type = request.POST.get('type')
        user = request.COOKIES["username"]
        d = certiRequest.objects.filter(uid = user, iid = insti, type = type)
        if not d.exists():
            r = certiRequest.objects.create(uid = user, iid = insti, type = type)
            r.save()
    return render(request, 'User/request.html')