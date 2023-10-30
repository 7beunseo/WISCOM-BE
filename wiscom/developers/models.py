from django.db import models
from posts.models import Post

class Developer(models.Model):
    post_number = models.ForeignKey(Post, related_name='developer', on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    image = models.ImageField(upload_to='developer_image')
    impression=models.TextField('IMPRESSION')
    

    def __str__(self):
        return self.name

