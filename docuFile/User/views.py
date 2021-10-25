from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from User.models import certiRequest
from login.models import CertiInfo
from Company.models import viewRequest
from pathlib import Path
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
@login_required(login_url = '/login')
def index(request):
    return render(request, 'User/home.html')

def dec_img(path,key):
    fin = open("media/"+path, 'rb')
    image = fin.read()
    fin.close()
    image = bytearray(image)
    for index, values in enumerate(image):
        image[index] = values ^ key
    return image

def download(request):
    key = int(request.GET['pkey'])
    path = request.GET['path']
    payload = dec_img(path,key)
    response = HttpResponse(bytes(payload), headers={ 'Content-Type': 'application/octet-stream', 'Content-Disposition': 'attachment; filename="'+path+'"'})
    return response

def home(request):
    user = CertiInfo.objects.filter(user = request.COOKIES["username"])
    key = int(request.POST.get('private_key'))
    fname = []
    for i in user:
        fname.append(i.certi)
    context = {
        'user': user,
        'username': request.COOKIES["username"],
        'private_key': key,
        'names':fname,
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

def send_mail(imail,key,user):
    subject = 'Welcome to docuFile'
    message = f'Hi,\n'+user+' is requested for some document.\nPrivate key for that is '+str(key)+' .\n\nRegards,\ndocuFile.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [imail]
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.send()

def request(request):
    if request.method == 'POST':
        insti = request.POST.get('iid')
        type = request.POST.get('type')
        user = request.COOKIES["username"]
        key = request.POST.get('private_key')
        d = certiRequest.objects.filter(uid = user, iid = insti, type = type)
        imail = User.objects.filter(username=insti)[0].email
        fname = User.objects.filter(username=user)[0].first_name
        lname = User.objects.filter(username=user)[0].last_name
        send_mail(imail,key,fname+' '+lname)
        if not d.exists():
            r = certiRequest.objects.create(uid = user, iid = insti, type = type)
            r.save()
    return render(request, 'User/request.html')