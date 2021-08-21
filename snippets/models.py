from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __repr__(self):
        return f"<User username={self.username}>"

    def __str__(self):
        return self.username

class Snippet(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=255, blank=True, null=True)
    snippet = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)