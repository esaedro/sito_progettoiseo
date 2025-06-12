
# Create your views here.
from django.shortcuts import render

def eventi_home(request):
    return render(request, 'eventi.html')
