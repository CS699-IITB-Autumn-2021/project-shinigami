from django.shortcuts import render
from login.models import CertiInfo
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def index(request):
    user = CertiInfo.objects.filter(user = 'vinnni002');
    src = os.path.join(BASE_DIR, 'media/')
    context = {
        'user': user[0]
    }
    return render(request, 'User/index.html', context)