from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import UserType, CertiInfo
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
import random
from django.conf import settings
from django.core.mail import EmailMessage
import os

# Create your views here.


def index(request):
    """ Loads the Login index-page template

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the Login indexpage

	"""
    return render(request, 'index.html')

def gen_pdf(uname,key):
    """ Generates the pdf file to be sent to a User upon registration which contains their private key.
    
    :param uname: username of User
    :param key: private key of User
    :returns: None

	"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "Hi,thank you for registering in docuFile.", ln = 1, align = 'L')
    pdf.cell(200, 10, txt = "Your private key is "+str(key),ln = 2, align = 'L')
    pdf.cell(200, 10, txt = "Please note that this private key is not stored in our servers.",ln = 3, align = 'L')
    pdf.cell(200, 10, txt = "Hence you are supposed to keep this safe with you at all times.",ln = 4, align = 'L')
    pdf.cell(200, 10, txt = "The Institute/Company you give access to your docs will also need this private key to ",ln = 5, align = 'L')
    pdf.cell(200, 10, txt = "view your documents.",ln = 6, align = 'L')
    pdf.cell(200, 10, txt = "So you will also have to share this with them.",ln = 6, align = 'L')
    pdf.output(str(uname)+".pdf")

def enc_pdf(uname,passwd):
    """ Encrypts the pdf file to be sent to a User upon registration with their account password as the pdf password.
    
    :param uname: username of User
    :param key: private key of User
    :returns: None

	"""
    out = PdfFileWriter()
    file = PdfFileReader(uname+".pdf")
    num = file.numPages
    for idx in range(num):
        page = file.getPage(idx)
        out.addPage(page)
    out.encrypt(passwd)
    with open(uname+".pdf", "wb") as f:
        out.write(f)

def gen_mail(uname,email,user_type):
    """ Generates the email to be sent to User or Institute upon registration. If it is a User, it also attaches a 
    password protected pdf file that contains their private key.
    
    :param uname: username of User or Institute
    :param email: email of User or Institute
    :param user_type: whether it is an User or an Institute
    :returns: None

	"""
    if user_type=="Personal":
        subject = 'Welcome to docuFile'
        message = f'Hi , thank you for registering in docuFile.\nYour private key is in the attach file.\nPassword of that file in your acc. password.\n\nRegards,\ndocuFile.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.attach_file(uname+'.pdf')
        email.send()
    else:
        subject = 'Welcome to docuFile'
        message = f'Hi , thank you for registering in docuFile.\n\nRegards,\ndocuFile.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.send()

def register(request):
    """ Signs up a User or Institute on the webapp

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the Login page or Signup page depending on whether it was a valid registration

	"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_type = request.POST.get('user_type', '')
            user_name = request.POST.get('username', '')
            passwd = request.POST.get('password1')
            email = request.POST.get('email')
            form.save()
            t = User.objects.get(username=user_name)
            u = UserType.objects.get(user_id=t.id)
            u.user_type = user_type
            u.user_name = user_name
            u.save()
            if user_type=="Personal":
                gen_pdf(user_name,key = random.randint(1, 100))
                enc_pdf(user_name,passwd)
                gen_mail(user_name,email,user_type)
                os.remove(user_name+".pdf")
            else:
                gen_mail(user_name,email,user_type)
            return render(request, 'index.html')
        else:
            return render(request, 'register.html', {"msg": form.errors})
    else:
        form = SignUpForm()
        args = {'form': form, "msg": form.errors}
        return render(request, 'register.html', args)


def auth_view(request):
    """ Authenticates the login of a User or Institute on the webapp

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the response

	"""
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        u = UserType.objects.filter(user_name=username)
        request.session['user_type'] = u[0].user_type
        request.session['basefile'] = u[0].user_type+"base.html"
        if u[0].user_type == 'Institute':
            response =  HttpResponseRedirect('/Company')
            response.set_cookie("compname",u[0].user_name)
            return response
        elif u[0].user_type == 'Personal':
            response =  HttpResponseRedirect('/User')
            response.set_cookie("username",u[0].user_name)
            return response
        else:
            #context = {'user': u}
            return render('errorpage.html')
    else:
        return HttpResponseRedirect('/login/invalidlogin/')


def invalidlogin(request):
    """ Loads invalid login webpage template

    :param request: The request object used to generate this response
    :returns: HttpResponse object with the invalid login page

	"""
    context = {"error": "enter valid username or password"}
    return render(request, 'invalidlogin.html', context)
