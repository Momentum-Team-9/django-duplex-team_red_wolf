from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def index(request):
    users = User.objects.all()
    return render(request, 'snippets/index.html', {'users': users})