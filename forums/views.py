# Create your views here.

from django.http import HttpResponse

# General index
def index(request):
	return HttpResponse("Hello, world. Saatana.")

# Shows contents of a single thread
def show_thread(request, thread_id):
	return HttpResponse("You're looking at thread %s." % thread_id)

# Shows contents of a single post
def show_post(request, post_id):
	return HttpResponse("You're looking at post %s." % post_id)

# Lets you add a new post
def add_post(request):
	return HttpResponse("You're trying to add a new post.")

# Lets you edit a post
def edit_post(request, post_id):
	return HttpResponse("You're trying to edit post %s." % post_id)
