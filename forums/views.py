# Create your views here.

from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render

from forums.models import Post, Subforum

# General index
def index(request):
    forum_list = Subforum.objects.filter(parent=None)

    template = loader.get_template('forums/index.html')
    context  = {'forum_list': forum_list}
    return render(request, 'forums/index.html', context)

# Shows contents of a (sub)forum
def show_forum(request, forum_id):
    # First try finding the (sub)forum
    forum = get_object_or_404(Subforum, pk=forum_id)

    # Start the list of the threads / subforums
    thread_list = "<ul>"

    # Grab all subforums that are children of this forum
    for sf in Subforum.objects.filter(parent=forum_id):
        thread_list += "<li>" + sf.title + "</li>" # Add them to the list

    # Grab all threads of the subforum in a newer-first order
    for t in Post.objects.filter(subforum=forum_id).filter(parent=None).order_by('-pub_date'):
        thread_list += "<li>" + t.title + "</li>" # Add them to the list
    # End the list of the threads
    thread_list += "</ul>"

    # Render test page
    if forum.is_root_cat():
        return HttpResponse("<h1>%s</h1><p>%s</p>" % (forum.title, thread_list))
    else:
        return HttpResponse("<h1>%s :: %s</h1><p>%s</p>" % (forum.parent.title, forum.title, thread_list))

# Shows contents of a single thread
def show_thread(request, thread_id):
    return HttpResponse("You're looking at thread %s." % thread_id)

# Shows contents of a single post
def show_post(request, post_id):
    # first try finding the post and grab it
    post = get_object_or_404(Post, pk=post_id)
    # Render it
    if post.is_op():
        return HttpResponse("<h1>%s :: %s</h1><p>%s</p>" % (post.subforum.title, post.title, post.content))
    else:
        return HttpResponse("<h1>%s :: %s :: %s</h1><p>%s</p>" % (post.subforum.title, post.parent.title, post.title, post.content))

# Lets you add a new post
def add_post(request):
    return HttpResponse("You're trying to add a new post.")

# Lets you edit a post
def edit_post(request, post_id):
    return HttpResponse("You're trying to edit post %s." % post_id)
