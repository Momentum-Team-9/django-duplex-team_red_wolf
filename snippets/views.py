import snippets
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Snippet
from .forms import SnippetForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
    all_snippets = Snippet.objects.all()
    snippets = []
    for snippet in all_snippets:
        if snippet.author == request.user:
            snippets.append(snippet)
    return render(request, "snippets/profile.html",
                {'snippets': snippets})

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    snippets = user.snippets.filter(public=True)
    
    return render(request, "snippets/user_profile.html", {"snippets": snippets, "username": username})

@login_required
def add_snippet(request):
    if request.method == 'GET':
        form = SnippetForm()
    else:
        form = SnippetForm(data=request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
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

def search(request):
    query = request.GET.get("query")
    search_results = Snippet.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(lang__icontains=query), public=True)

    return render(request, "snippets/main_page.html", {"snippets": search_results})