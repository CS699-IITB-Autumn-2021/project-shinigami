from django.shortcuts import render

from login.models import CertiInfo

# Create your views here.
def index(request):
    return render(request, 'Company/index.html')

def issue(request):
    if request.method == 'POST':
        username = request.POST.get('uid')
        typeC = request.POST.get('type')
        image = request.POST.get('certificate')
        userC = CertiInfo(user=username, type=typeC, certi=image)
        userC.save() 
    return render(request, 'Company/issue.html')