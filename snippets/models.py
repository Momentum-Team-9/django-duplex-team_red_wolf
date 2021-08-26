from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __repr__(self):
        return f"<User username={self.username}>"

    def __str__(self):
        return self.username


LANGUAGES = (
    ("markup", "MARKUP"),
    ("css", "CSS"),
    ("clike", "C+"),
    ("javascript", "JAVASCRIPT"),
    ("csharp", "C#"),
    ("csv", "CSV"),
    ("git", "GIT"),
    ("http", "HTTP"),
    ("java", "JAVA"),
    ("python", "PYTHON"),
    ("sql", "SQL"),
)


class Snippet(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(
        choices=LANGUAGES, max_length=11, default=None, blank=True, null=True
    )
    snippet = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="snippets")
    original_snippet = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="snippet_copies"
    )

    def __str__(self):
        return f"{self.title}"
