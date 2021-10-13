from django.shortcuts import render
from django.contrib.auth.models import User
from login.models import CertiInfo
from PIL import Image

# Create your views here.
def index(request):
    return render(request, 'Company/index.html')

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