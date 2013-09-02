from django.db                  import models
from django.contrib.auth.models import User
from django.forms               import ModelForm

# The database models for the forum

_max_length = 200

class Subforum(models.Model):
    # if parent == null, this is a root subforum
    parent      = models.ForeignKey('self', null=True, blank=True)
    # title of the subforum
    title       = models.CharField(max_length=_max_length)
    # description of the subforum
    description = models.CharField(max_length=_max_length, blank=True)
    def is_root_cat(self):
        return (self.parent is None)
    def __unicode__(self):
        return self.title

class Thread(models.Model):
    # subforum in which this thread is located
    subforum      = models.ForeignKey(Subforum)
    # the user who created this thread originally
    creator       = models.ForeignKey(User)
    op            = models.ForeignKey('Post', related_name='+')
    title         = models.CharField(max_length=_max_length)
    creation_date = models.DateTimeField('date created')
    # whether or not this thread will be stuck on the top of the thread listing
    sticky        = models.BooleanField()
    def __unicode__(self):
        return self.title

class Post(models.Model):
    # thread in which this post is located
    thread   = models.ForeignKey(Thread)
    # the user who posted this post
    poster   = models.ForeignKey(User)
    # content below
    title    = models.CharField(max_length=_max_length)
    content  = models.TextField()
    pub_date = models.DateTimeField('date posted')
    def __unicode__(self):
            return self.content[:50]

# Model-to-form generators

class SubforumForm(ModelForm):
    class Meta:
        model  = Subforum
        fields = ['parent', 'title', 'description']
