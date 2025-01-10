from django.db import models                                                                                                  # type: ignore
from django.contrib.auth.models import User                                                                                   # type: ignore

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)  

    def __str__(self):
        return self.title