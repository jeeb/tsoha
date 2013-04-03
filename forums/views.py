# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from forums.models import Post

# General index
def index(request):
	return HttpResponse("Hello, world. Saatana.")

# Shows contents of a (sub)forum
def show_forum(request, forum_id):
	return HttpResponse("You're looking at forum %s." % forum_id)

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
