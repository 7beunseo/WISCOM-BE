from django.db import models
from django.conf import settings


# Create your models here.
class Post(models.Model):
    title = models.CharField('TITLE', max_length=50)
    content = models.TextField('CONTENT')
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()