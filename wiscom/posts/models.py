from django.db import models
import os

def post_image_upload_path(instance, filename):
    return f'post_{instance.post.id}/{filename}'

def post_logo_upload_path(instance, filename):
    # 이미지 파일을 'logo' 폴더에 저장
    return f'logo/{filename}'

class Tag(models.Model):
    CATEGORY={
        ('posts','posts'),
        ('comments','comments')
    }
    category = models.CharField(verbose_name="tag_type", default='', max_length=10, choices=CATEGORY)
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
    team = models.CharField('TEAM', max_length=50)
    content = models.TextField('CONTENT')
    likes = models.IntegerField('LIKE', default=0)
    logo = models.ImageField('LOGO', upload_to=post_logo_upload_path)
    service_url = models.URLField('SERVICE_URL', max_length=200)

    def __str__(self):
        return self.title


class Photo(models.Model):
    post = models.ForeignKey(Post, related_name='post_image', on_delete=models.CASCADE, null=True)
    image = models.ImageField('IMAGE', upload_to=post_image_upload_path)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_tags = models.ManyToManyField(CommentTag, blank=True)
    content = models.TextField('CONTENT')
    created_at = models.DateTimeField('CREATED_AT', auto_now_add=True)

    def __str__(self):
        return self.content


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField('IP')

    def __str__(self):
        return f'Like for Post {self.post.id} from {self.ip}'