from django.shortcuts import render, redirect
from .models import User, Snippet

# Create your views here.
def index(request):
    users = User.objects.all()
    if request.user.is_authenticated:
        return redirect('main_page')
    return render(request, 'snippets/index.html', {'users': users})


def main_page(request):
    snippets = Snippet.objects.all()
    return render(request, "snippets/main_page.html",
                  {'snippets': snippets})

def profile(request):
    snippets = Snippet.objects.all()
    return render(request, "snippets/profile.html",
                  {'snippets': snippets})