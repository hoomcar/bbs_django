from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class Link(models.Model):
#    url=models.URLField(unique=True)

#class Content(models.Model):
#    content = models.TextField()

class List(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    date = models.DateTimeField()
#    date = models.DateField()
    content = models.TextField()
    how_many_views = models.IntegerField()
    
#class Comment(models.Model):
#    parent_id = models.IntegerField()
#    comment = models.CharField(max_length=255)
#    user = models.ForeignKey(User)
#    date = models.DateTimeField()