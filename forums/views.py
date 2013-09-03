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

from forums.models import Post, Thread, Subforum, SubforumForm

# General index
def index(request):
    # Grab all root forums
    forum_list = Subforum.objects.filter(parent=None)

    # Load template and set context
    template = loader.get_template('forums/index.html')
    context  = {'forum_list': forum_list,
                'title': "Forum index"}

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
        threads = threads.exclude(id__in=sticky_threads)

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

@login_required()
def add_forum(request):
    # Load template
    template = loader.get_template('forums/add_forum.html')

    # TODO: Implement proper error page
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse(index))

    if request.method == 'POST':
        # Try to create a form from the POST data
        form = SubforumForm(request.POST)

        if form.is_valid():
            parent      = form.cleaned_data['parent']
            title       = form.cleaned_data['title']
            description = form.cleaned_data['description']

            f = Subforum(parent=parent, title=title,
                         description=description)
            if not f:
                return render(request, 'forums/add_forum.html', {
                    'form': form,
                    'error_message': "Subforum object creation failed :< !"
                    })

            f.save()
            return HttpResponseRedirect(reverse(add_forum))
        else:
            return render(request, 'forums/add_forum.html', {
                'form': form,
                'error_message': "Invalid data :< !"
                })
    else:
        form = SubforumForm()
        return render(request, 'forums/add_forum.html', {
            'form': form,
            })

# Shows contents of a single thread
def show_thread(request, thread_id):
    # First try finding the thread and grab its posts ordered older-first
    thread = get_object_or_404(Thread, pk=thread_id)
    posts  = Post.objects.filter(thread=thread_id).order_by('pub_date')

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
                    is_op=True, pub_date=timezone.now())
            if not p:
                t.delete()
                return render(request, 'forums/add_thread.html', {
                    'forum': forum,
                    'error_message': "Gooby please... I have no idea what just happened, but you errored out (post object creation).",
                    })

            p.save()

            # For good measure, do a HttpResponseRedirect
            return HttpResponseRedirect(reverse(show_thread, args=(t.id,)))
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
    thread = get_object_or_404(Thread, pk=thread_id)

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
            p = Post(thread=thread, poster=request.user, title=title,
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
@login_required()
def edit_post(request, post_id):
    # First try finding the post and thread
    post   = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread, pk=post.thread.id)

    # One can only edit his/her own posts
    if request.user != post.poster:
        return HttpResponse("Not correct user %s , post owned by %s !" % ( request.user.username, post.poster.username ))

    # Load the template
    template = loader.get_template('forums/edit_post.html')

    # We do different things for POST and GET
    if request.method == 'POST':
        # Grab the info from the post thingy
        try:
            title   = request.POST['title']
            content = request.POST['content']
        # If something goes wrong...
        except (KeyError):
            return render(request, 'forums/edit_post.html', {
                'post': post,
                'error_message': "You didn't provide needed data!",
                })
        # If we get both info out well?
        else:
            # If content is empty, error out
            if not content:
                return render(request, 'forums/edit_post.html', {
                    'post': post,
                    'error_message': "Please do not leave content empty :< !",
                    })

            # If content is there, push it to the object
            post.content = content

            # What to do if we do not have a title set?
            if not title:
                # If it's an OP, we need to copy the thread title
                if post.is_op:
                    title = thread.title
                # Otherwise we'll just use Re: <thread title>
                else:
                    title = "Re: " + thread.title
            else:
                # And if we have a title, and the post is an OP
                # we set the thread title as well to match the
                # post's
                if post.is_op:
                    thread.title = title
                    thread.save()

            post.title = title

            post.save()

            return HttpResponseRedirect(reverse(show_thread, args=(thread.id,)))
    # And here is what GET n' shit does (endif method == POST)
    else:
        return render(request, 'forums/edit_post.html', {
            'post': post,
            })

# Lets you remove a post
@login_required()
def remove_post(request, post_id):
    # First try finding the post and thread
    post   = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread, pk=post.thread.id)

    subforum = thread.subforum

    # One can only edit his/her own posts
    if request.user != post.poster:
        return HttpResponse("Not correct user %s , post owned by %s !" % ( request.user.username, post.poster.username ))

    if post.is_op:
        Post.objects.filter(thread=thread).delete()
        thread.delete()
        return HttpResponseRedirect(reverse(show_forum, args=(subforum.id,)))
    else:
        post.delete()
        return HttpResponseRedirect(reverse(show_thread, args=(thread.id,)))


# Search functionality
def search(request):
    return HttpResponse("You're trying to search.")
