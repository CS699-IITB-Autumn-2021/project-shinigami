from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import UserType,CertiInfo
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user_type = request.POST.get('user_type','')
            user_name = request.POST.get('username', '')
            print(user_type)
            form.save()
            if user_type=="Personal":
                x = User.objects.get(username=user_name)
                y = CertiInfo.objects.get(user_id=x.id)
                y.user_name=user_name
                y.certi = ""
                y.save()
            t = User.objects.get(username=user_name)
            u = UserType.objects.get(user_id=t.id)
            u.user_type=user_type
            u.user_name=user_name
            u.save()
            return render(request,'index.html')
        else:
            return render(request,'register.html',{"msg":form.errors})        
    else:
        form = SignUpForm()
        args = {'form': form,"msg":form.errors}
        return render(request, 'register.html', args)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	print(user)
	if user is not None:
	    auth.login(request,user)
	    u = UserType.objects.filter(user_name=username)
	    request.session['user_type'] = u[0].user_type
	    request.session['basefile'] = u[0].user_type+"base.html"
	    if u[0].user_type=='Institute':
	    	return HttpResponseRedirect('/Company')
	    elif u[0].user_type=='Personal':
	    	request.session["username"]=u[0].user_name
	    	return HttpResponseRedirect('/User')
	    else:
            #context = {'user': u}
	        return render('errorpage.html')
	else:
		return HttpResponseRedirect('/login/invalidlogin/')

def invalidlogin(request):
    context = {"error":"enter valid username or password"}
    return render(request,'invalidlogin.html',context)
