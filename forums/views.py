# Create your views here.

from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render

from forums.models import Post, Subforum

# General index
def index(request):
    # Grab all root forums
    forum_list = Subforum.objects.filter(parent=None)

    # Load template and set context
    template = loader.get_template('forums/index.html')
    context  = {'forum_list': forum_list}

    # Render the view
    return render(request, 'forums/index.html', context)

# Shows contents of a (sub)forum
def show_forum(request, forum_id):
    # First try finding the (sub)forum
    forum = get_object_or_404(Subforum, pk=forum_id)

    # Grab all subforums that are children of this forum
    subforums = Subforum.objects.filter(parent=forum_id)
    # Grab all threads of the current (sub)forum in a newer-first order
    threads   = Post.objects.filter(subforum=forum_id).filter(parent=None).order_by('-pub_date')

    # Load template and set context
    template = loader.get_template('forums/show_forum.html')
    context  = {
        'forum':     forum,
        'subforums': subforums,
        'threads':   threads,
    }

    # Render the view
    return render(request, 'forums/show_forum.html', context)

# Shows contents of a single thread
def show_thread(request, thread_id):
    return HttpResponse("You're looking at thread %s." % thread_id)

# Shows contents of a single post
def show_post(request, post_id):
    # first try finding the post and grab it
    post = get_object_or_404(Post, pk=post_id)

    # Load template and set context
    template = loader.get_template('forums/show_post.html')
    context  = {
        'post': post,
    }

    # Render the view
    return render(request, 'forums/show_post.html', context)

# Lets you add a new post
def add_post(request):
    return HttpResponse("You're trying to add a new post.")

# Lets you edit a post
def edit_post(request, post_id):
    return HttpResponse("You're trying to edit post %s." % post_id)
