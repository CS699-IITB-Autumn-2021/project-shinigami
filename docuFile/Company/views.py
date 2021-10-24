from django.shortcuts import render, redirect
from Company.models import viewRequest
from User.models import certiRequest
from login.models import CertiInfo
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

import random

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect

@login_required(login_url = '/login')
def index(request):
    d = certiRequest.objects.filter(iid = request.COOKIES["compname"])
    for i in d:
        t = CertiInfo.objects.filter(user = i.uid, insti = i.iid, type = i.type)
        print(i.uid)
        print(i.iid)
        print(i.type)
        if t.exists():
            print('yes')
            i.delete()

    context = {
        'data': d
    }
    
    if request.method == 'POST':
        data = request.POST
        count = 1
        for i in data.keys():
            if count == 2:
                n = i
            count += 1 
        dec = n.split('_')[0]
        user = n.split('_')[1]
        type = n.split('_')[2]
        if dec == 'issue':
            return redirect('/Company/issue')
        if dec == 'decline':
            r = certiRequest.objects.get(uid = user, type = type, iid = request.COOKIES["compname"])
            r.delete()
    return render(request, 'Company/index.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('http://localhost:8000')

def enc_img(img,key):
    # performing XOR operation on each value of bytearray
    fin = open("media/"+img, 'rb')
    image = fin.read()
    fin.close()
    image = bytearray(image)
    for index, values in enumerate(image):
        image[index] = values ^ key
    fin = open("media/"+img, 'wb')
    fin.write(image)
    fin.close()

def issue(request):
    if request.method == 'POST':
        username = request.POST.get('pid')
        print(username)
        user = User.objects.get(username = username)
        if user != None:
            typeC = request.POST.get('type')
            image = request.FILES['certificate']
            userC = CertiInfo.objects.create(user=username,insti = request.COOKIES["compname"],type=typeC, certi=image)
            userC.save()
            #enc_img(request.FILES['certificate'].name,key)

    return render(request, 'Company/issue.html')

def request(request):
    if request.method == 'POST':
        user = User.objects.get(username = request.POST.get('pid'))
        insti = User.objects.get(username = request.COOKIES["compname"])
        # print(insti)
        if user != None:
            d = viewRequest.objects.filter(uid = request.POST.get('pid'), ifirst = insti.first_name,ilast = insti.last_name)
            if not d.exists():
                req = viewRequest.objects.create(ifirst = insti.first_name, ilast = insti.last_name, uid = user, status = 'NA')
    return render(request, 'Company/request.html')

def pending(request):
    insti = User.objects.get(username = request.COOKIES["compname"])
    req = viewRequest.objects.filter(status = 'NA', ifirst = insti.first_name, ilast = insti.last_name)
    context = {
        'req': req
    }
    if request.method == 'POST':
        data = request.POST
        count = 1
        for i in data.keys():
            if count == 2:
                n = i
            count += 1
        r = viewRequest.objects.get(ifirst = insti.first_name, ilast = insti.last_name, uid = n)
        r.delete()
    return render(request, 'Company/pending.html', context)