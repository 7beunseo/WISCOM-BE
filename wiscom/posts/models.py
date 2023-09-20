from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField('TITLE', max_length=50)
    content = models.TextField('CONTENT')
    likes = models.IntegerField('LIKE', default=0)

    def __str__(self):
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField('CONTENT')
    created_at = models.DateTimeField('CREATED_AT', auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField('IP')