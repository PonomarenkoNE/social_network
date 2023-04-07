from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_request = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

    def count_likes(self):
        return self.likes.count()


class Like(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
