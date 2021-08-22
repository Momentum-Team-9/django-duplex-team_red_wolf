import snippets
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Snippet
from .forms import SnippetForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    users = User.objects.all()
    if request.user.is_authenticated:
        return redirect('main_page')
    return render(request, 'snippets/index.html', {'users': users})

@login_required
def main_page(request):
    all_snippets = Snippet.objects.all()
    snippets = []
    for snippet in all_snippets:
        if snippet.public == True:
            snippets.append(snippet)
    return render(request, "snippets/main_page.html",
                {'snippets': snippets})

@login_required
def profile(request):
    snippets = Snippet.objects.all()
    return render(request, "snippets/profile.html",
                {'snippets': snippets})

@login_required
def add_snippet(request):
    if request.method == 'GET':
        form = SnippetForm()
    else:
        form = SnippetForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='profile')

    return render(request, "snippets/add_snippet.html", {"form": form})

@login_required
def edit_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.method == 'GET':
        form = SnippetForm(instance=snippet)
    else: 
        form = SnippetForm(data=request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect(to='profile')

    return render(request, 'snippets/edit_snippet.html', {'form': form, 'snippet': snippet})

@login_required
def delete_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.method == 'POST':
        snippet.delete()
        return redirect(to='list_snippets')

    return render(request, "snippets/delete_snippet.html",
        {"snippet": snippet})