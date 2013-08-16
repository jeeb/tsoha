# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from forums.models import Post, Thread, Subforum

# General index
def index(request):
    # Grab all root forums
    forum_list = Subforum.objects.filter(parent=None)

    # Load template and set context
    template = loader.get_template('forums/index.html')
    context  = {'forum_list': forum_list}

    # Render the view
    return render(request, 'forums/index.html', context)

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse(index))

    template = loader.get_template('forums/register.html')

    # We do different things for POST and GET
    if request.method == 'POST':
        # Grab the info from the request
        try:
            user_name    = request.POST['user_name']
            email        = request.POST['email']
            password_1st = request.POST['password_1st']
            password_2nd = request.POST['password_2nd']
        # If something goes wrong...
        except (KeyError):
            return render(request, 'forums/register.html', {
                'error_message': "You didn't provide needed data!",
                })

        # Do not let user register if there's not enough information
        if not user_name or not password_1st or not password_2nd:
            return render(request, 'forums/register.html', {
                'error_message': "Gooby please... No empty user names or passwords.",
                })

        # Do not let user register if there's already a user with that username
        if User.objects.filter(username=user_name).count():
            return render(request, 'forums/register.html', {
                'error_message': "User name already exists in system, please select another user name.",
                })

        # Check password inputs for equality
        if password_1st != password_2nd:
            return render(request, 'forums/register.html', {
                'error_message': "Gooby please... Your passwords do not match.",
                })

        # Set the final password variable
        password = password_1st

        # Do not let user to register if user name and password match
        if password == user_name:
            return render(request, 'forums/register.html', {
                'error_message': "Gooby please... Do not use your exact user name as password.",
                })

        # After clearing all those obstacles we create a user!
        User.objects.create_user(username=user_name, email=email, password=password)

        user = authenticate(username=user_name, password=password)

        # If the creation seems to have been successful...
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(index))
        else:
            return render(request, 'forums/register.html', {
                'error_message': "Gooby please... I have no idea what just happened, but you errored out.",
                })
    # GET stuff down here
    else:
        return render(request, 'forums/register.html')

# Shows contents of a (sub)forum
def show_forum(request, forum_id):
    # First try finding the (sub)forum
    forum = get_object_or_404(Subforum, pk=forum_id)

    # Grab all subforums that are children of this forum
    subforums = Subforum.objects.filter(parent=forum_id)

    # Grab all threads of the current (sub)forum in a newer-first order
    threads   = Thread.objects.filter(subforum=forum_id).order_by('-creation_date')

    # Get all sticky threads
    sticky_threads = threads.filter(sticky=True)

    # And then remove sticky threads from the list of threads
    if sticky_threads.count() != 0:
        threads = threads.exclude(sticky_threads)

    # Load template and set context
    template = loader.get_template('forums/show_forum.html')
    context  = {
        'forum':          forum,
        'subforums':      subforums,
        'sticky_threads': sticky_threads,
        'threads':        threads,
    }

    # Render the view
    return render(request, 'forums/show_forum.html', context)

# Shows contents of a single thread
def show_thread(request, thread_id):
    # First try finding the thread and grab its posts ordered older-first
    thread = get_object_or_404(Post, pk=thread_id, parent=None)
    posts  = Post.objects.filter(Q(parent=thread_id) | Q(pk=thread_id)).order_by('pub_date')

    # Load template and set context
    template = loader.get_template('forums/show_thread.html')
    context  = {
        'thread': thread,
        'posts':  posts,
    }

    return render(request, 'forums/show_thread.html', context)

# Lets you add a new thread into a (sub)forum
@login_required()
def add_thread(request, forum_id):
    # First try finding the (sub)forum
    forum = get_object_or_404(Subforum, pk=forum_id)

    # Load template
    template = loader.get_template('forums/add_thread.html')

    # We do different things for POST and GET
    if request.method == 'POST':
        # Grab the info from the post thingy
        try:
            title   = request.POST['title']
            content = request.POST['content']
        # If something goes wrong...
        except (KeyError):
            return render(request, 'forums/add_thread.html', {
                'forum': forum,
                'error_message': "You didn't provide needed data!",
                })
        # If we get both info out well?
        else:
            # If content is empty, error out
            if not content or not title:
                return render(request, 'forums/add_thread.html', {
                    'forum': forum,
                    'error_message': "Please do not leave content or title empty :< !",
                    })

            # Create and write post into the database, wee
            t = Thread(subforum=Subforum.objects.get(pk=forum.id),
                       creator=request.user, title=title, creation_date=timezone.now(),
                       sticky=False)
            if not t:
                return render(request, 'forums/add_thread.html', {
                    'forum': forum,
                    'error_message': "Gooby please... I have no idea what just happened, but you errored out (thread object creation).",
                    })

            t.save()

            p = Post(thread=t, poster=request.user, title=title, content=content,
                     pub_date=timezone.now())
            if not p:
                t.delete()
                return render(request, 'forums/add_thread.html', {
                    'forum': forum,
                    'error_message': "Gooby please... I have no idea what just happened, but you errored out (post object creation).",
                    })

            p.save()

            # For good measure, do a HttpResponseRedirect
            return HttpResponseRedirect(reverse(show_thread, args=(p.id,)))
    else:
        return render(request, 'forums/add_thread.html', {
            'forum': forum
            })

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
@login_required()
def add_post(request, thread_id):
    # First try finding the thread
    thread = get_object_or_404(Post, pk=thread_id, parent=None)

    # Load template
    template = loader.get_template('forums/add_post.html')

    # We do different things for POST and GET
    if request.method == 'POST':
        # Grab the info from the post thingy
        try:
            title   = request.POST['title']
            content = request.POST['content']
        # If something goes wrong...
        except (KeyError):
            return render(request, 'forums/add_post.html', {
                'thread': thread,
                'error_message': "You didn't provide needed data!",
                })
        # If we get both info out well?
        else:
            # If content is empty, error out
            if not content:
                return render(request, 'forums/add_post.html', {
                    'thread': thread,
                    'error_message': "Please do not leave content empty :< !",
                    })

            # If title is empty we just use Re: <thread title>
            if not title:
                title = "Re: " + thread.title

            # Create and write post into the database, wee
            p = Post(subforum=Subforum.objects.get(pk=thread.subforum.id),
                     parent=Post.objects.get(pk=thread.id), title=title,
                     content=content, pub_date=timezone.now())
            p.save()

            # For good measure, do a HttpResponseRedirect
            return HttpResponseRedirect(reverse(show_thread, args=(thread.id,)))
    # And here is what GET n' shit does
    else:
        return render(request, 'forums/add_post.html', {
            'thread': thread,
            })

# Lets you edit a post
def edit_post(request, post_id):
    return HttpResponse("You're trying to edit post %s." % post_id)
