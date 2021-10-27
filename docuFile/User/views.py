from django.shortcuts import render, redirect
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
    """ Loads the User index-page template

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the User indexpage

	"""
    context = {
        'name': request.COOKIES["username"]
    }
    return render(request, 'User/home.html', context)

def dec_img(path,key):
    """ Decrypts an encrypted document by performing XOR using the private key of the User

    :param path: path to encrypted image (document)
    :param key: private key of User
    :returns: decrypted image (document)

	"""
    fin = open("media/"+path, 'rb')
    image = fin.read()
    fin.close()
    image = bytearray(image)
    for index, values in enumerate(image):
        image[index] = values ^ key
    return image

def download(request):
    """ Downloads the decrypted document of an User

    :param request: The request object used to generate this HttpResponse
    :returns: decrypted image download response

	"""
    key = int(request.GET['pkey'])
    path = request.GET['path']
    payload = dec_img(path,key)
    response = HttpResponse(bytes(payload), headers={ 'Content-Type': 'application/octet-stream', 'Content-Disposition': 'attachment; filename="'+path+'"'})
    return response

def home(request):
    """ Loads the User home-page template

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the User homepage

	"""
    user = CertiInfo.objects.filter(user = request.COOKIES["username"])
    key = int(request.POST.get('private_key'))
    context = {
        'user': user,
        'username': request.COOKIES["username"],
        'private_key': key,
        'name': request.COOKIES["username"]
    }
    return render(request, 'User/index.html', context)

def logout(request):
    """ Logs out User from app

    :param request: The request object used to generate this response
    :returns: Redirect to log-in page

	"""
    auth.logout(request)
    return HttpResponseRedirect('http://localhost:8000')

def private(request):
    """ Asks for private key of user

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the enter private key page
	"""
    if request.method == 'POST':
        context = {
            'name': request.COOKIES["username"]
        }
        key = request.POST.get('private_key')
        response =  HttpResponseRedirect('/User/pending')
        response.set_cookie("pkey",key)
        return response
    return render(request, 'User/private.html')

def send_mail(imail,msg):
    """ Sends an email from a User to the Company or Institute whom User requests for a certificate.

    :param imail: email of Institute or Company that receives the request
    :param msg: msg to be sent in email
    :returns: None

	"""
    subject = 'Welcome to docuFile'
    message = msg
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [imail]
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.send()

def pending(request):
    """ Loads the pending view-request from Institute or Company and gives facility to User
    to either accept or reject the requests

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the pending-requests navbar open

	"""
    if request.method == 'POST':
        key = request.COOKIES["pkey"]
        print(key)
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
            imail = User.objects.filter(first_name=first,last_name=last)[0].email
            msg = f'Hi,\n'+request.COOKIES["username"]+' is granted your requested for document view.\nPrivate key for viewing documents is '+str(key)+' .\n\nRegards,\ndocuFile.'
            send_mail(imail,msg)
            r.status = 'A'
            r.save()
        elif dec == 'reject':
            r = viewRequest.objects.get(ifirst = first, ilast = last, uid = request.COOKIES["username"])
            r.delete()
    req = viewRequest.objects.filter(status = 'NA', uid = request.COOKIES["username"])
    context = {
        'req': req,
        'name': request.COOKIES["username"]
    }
    return render(request, 'User/pending.html', context)

def granted(request):
    """ Loads the list of Institute or Company who have been granted view-request and gives facility to User
    to remove the request either temporarily or permanently

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the granted view-requests navbar open

	"""
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
        'grant': granted,
        'name': request.COOKIES["username"]
    }
    return render(request, 'User/granted.html', context)

def request(request):
    """ Loads a webpage that can be used by User to request Institute or Company for some documents

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the request Certificate navbar open

	"""
    if request.method == 'POST':
        insti = request.POST.get('iid')
        type = request.POST.get('type')
        user = request.COOKIES["username"]
        key = request.POST.get('private_key')
        d = certiRequest.objects.filter(uid = user, iid = insti, type = type)
        imail = User.objects.filter(username=insti)[0].email
        fname = User.objects.filter(username=user)[0].first_name
        lname = User.objects.filter(username=user)[0].last_name
        msg = f'Hi,\n'+fname+' '+lname+' is requested for some document.\nPrivate key for that is '+str(key)+' .\n\nRegards,\ndocuFile.'
        send_mail(imail,msg)
        if not d.exists():
            r = certiRequest.objects.create(uid = user, iid = insti, type = type)
            r.save()
    
    context = {
        'name': request.COOKIES["username"]
    }

    return render(request, 'User/request.html', context)