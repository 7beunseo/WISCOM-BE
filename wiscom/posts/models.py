from django.db import models

class Tag(models.Model):
    CATEGORY={
        ('posts','posts'),
        ('comments','comments')
    }
    category = models.CharField(verbose_name="병원 주소", default='', max_length=10, choices=CATEGORY)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CommentTag(models.Model):
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
    comment_tags = models.ManyToManyField(CommentTag, blank=True)
    content = models.TextField('CONTENT')
    created_at = models.DateTimeField('CREATED_AT', auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField('IP')

    def __str__(self):
        return f'Like for Post {self.post.id} from {self.ip}'