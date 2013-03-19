from django.db import models

# Create your models here.

class Subforum(models.Model):
    # if parent == null, this is a root subforum
    parent = models.ForeignKey('self', null=True)
    # content below
    title  = models.CharField(max_length=200)

class Post(models.Model):
    # subforum in which this post is set
    subforum = models.ForeignKey(Subforum)
    # parent post, if null, this is a 'thread'
    parent   = models.ForeignKey('self', null=True)
    # content below
    title    = models.CharField(max_length=200)
    content  = models.TextField()
    pub_date = models.DateTimeField('date published')
