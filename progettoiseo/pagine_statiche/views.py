from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def storia(request):
    return render(request, 'storia.html')

def contatti(request):
    return render(request, 'contatti.html')

def direttivo(request):
    return render(request, 'direttivo.html')
