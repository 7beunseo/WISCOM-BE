from django.db import models

class Developer(models.Model):
    post_number = models.IntegerField(default=0)
    name = models.CharField(max_length=10)
    image = models.ImageField(upload_to='media/images/')
    

    def __str__(self):
        return self.name

