from django.db import models


# Create your models here.
class Guest(models.Model):
    created_dt = models.DateTimeField('CREATED_AT', auto_now_add=True)
    name = models.CharField(max_length=100)
    content = models.TextField()
    
    def __str__(self):
        return self.name