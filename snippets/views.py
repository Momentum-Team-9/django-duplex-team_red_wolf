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
        return redirect("main_page")
    return render(request, "snippets/index.html", {"users": users})


@login_required
def main_page(request):
    all_snippets = Snippet.objects.all()
    snippets = []
    for snippet in all_snippets:
        if snippet.public == True:
            snippets.append(snippet)
    return render(request, "snippets/main_page.html", {"snippets": snippets})


@login_required
def profile(request):
    user = get_object_or_404(User, username=request.user)
    profile_snippets = user.snippets.filter()

    return render(request, "snippets/profile.html", {"snippets": profile_snippets})


@login_required
def user_profile(request, username):
    snippets = request.user.snippets.filter(public=True)
    return render(
        request,
        "snippets/user_profile.html",
        {"snippets": snippets, "username": username, "user": request.user},
    )


@login_required
def add_snippet(request):
    if request.method == "GET":
        form = SnippetForm()
    else:
        form = SnippetForm(data=request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
            return redirect(to="profile")

    return render(request, "snippets/add_snippet.html", {"form": form})


@login_required
def edit_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.method == "GET":
        form = SnippetForm(instance=snippet)
    else:
        form = SnippetForm(data=request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect(to="profile")

    return render(
        request, "snippets/edit_snippet.html", {"form": form, "snippet": snippet}
    )


@login_required
def delete_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.method == "POST":
        snippet.delete()
        return redirect(to="profile")

    return render(request, "snippets/delete_snippet.html", {"snippet": snippet})


@login_required
def search(request):
    query = request.GET.get("query")
    search_results = Snippet.objects.filter(
        Q(title__icontains=query)
        | Q(author__username__icontains=query)
        | Q(lang__icontains=query),
        public=True,
    )

    return render(request, "snippets/main_page.html", {"snippets": search_results})


@login_required
def profile_search(request):
    user = get_object_or_404(User, username=request.user)
    profile_snippets = user.snippets.filter()
    query = request.GET.get("query")
    search_results = profile_snippets.filter(
        Q(title__icontains=query)
        | Q(author__username__icontains=query)
        | Q(lang__icontains=query)
    )

    return render(
        request,
        "snippets/profile.html",
        {"profile": profile, "snippets": search_results},
    )


@login_required
def copy_snippet(request, pk):
    original = get_object_or_404(Snippet, pk=pk)
    user = request.user
    if request.method == "POST":
        form = SnippetForm(data=request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.snippet = original.snippet
            snippet.original_snippet = original
            snippet.title = original.title
            snippet.lang = original.lang
            original.copy_count += 1
            original.save()
            snippet.save()
            return redirect("profile")
    else:
        form = SnippetForm()

    return render(request, "snippets/profile.html", {"form": form, "org": original})
