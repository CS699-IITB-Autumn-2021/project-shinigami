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
    """ Loads the Company index-page (homepage) template and also displays the pending
    Certificate requests

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the Company indexpage

	"""
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
            r = certiRequest.objects.filter(uid = user, type = type, iid = request.COOKIES["compname"])
            r.delete()

    d = certiRequest.objects.filter(iid = request.COOKIES["compname"])

    context = {
        'data': d
    }
    
    return render(request, 'Company/index.html', context)

def logout(request):
    """ Logs out Company from app

    :param request: The request object used to generate this response
    :returns: Redirect to log-in page

	"""
    auth.logout(request)
    return HttpResponseRedirect('http://localhost:8000')

def enc_img(img,key):
    """ Encrypts an encrypted document by performing XOR on each value of bytearray using 
    the private key of the User

    :param img: path to image (document)
    :param key: private key of User
    :returns: encrypted image (document)

	"""
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
    """ Adds certificate to an User by the Institute or Company while also encrypting the certificate

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the Issue certificate navbar open

	"""
    if request.method == 'POST':
        username = request.POST.get('pid')
        print(username)
        user = User.objects.get(username = username)
        if user != None:
            typeC = request.POST.get('type')
            image = request.FILES['certificate']
            key = int(request.POST.get('private_key'))
            userC = CertiInfo.objects.create(user=username,insti = request.COOKIES["compname"],type=typeC, certi=image)
            userC.save() 
            t = certiRequest.objects.filter(uid = username, type = typeC, iid = request.COOKIES["compname"])
            if t != None:
                t.delete()
            enc_img(request.FILES['certificate'].name,key)
    return render(request, 'Company/issue.html')

def request(request):
    """ Loads a webpage that can be used by Company or Institute to request User for view-permission of documents

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the request View-permission navbar open

	"""
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
    """ Loads the pending view-request to Users and gives facility to Institute or Company
    to Cancel the requests

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the pending-requests navbar open

	"""
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

def view(request):
    return render(request, 'Company/view.html')

def certificate(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        insti = User.objects.get(username = request.COOKIES["compname"])
        t = viewRequest.objects.get(ifirst = insti.first_name, ilast = insti.last_name, uid = pid)
        if t.status == 'A':
            cer = CertiInfo.objects.filter(user = pid)
            context = {
                'user': cer
            }
        else:
            context = {
                'user': None
            }
    return render(request, 'Company/certificate.html', context)