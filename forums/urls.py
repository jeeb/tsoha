from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout

from forums import views

urlpatterns = patterns('',
    # ex: /forums/
    url(r'^$', views.index, name='index'),
    # ex: /accounts/login/ , standard implementation
    url(r'^accounts/login/?$',  login, name='login'),
    # ex: /accounts/logout/ , standard implementation
    url(r'^accounts/logout/?$', logout, name='logout'),
    # ex: /logout
    url(r'^logout/?$', views.log_out, name='log_out'),
    # ex: /register
    url(r'^register/?$', views.register, name='register'),
    # ex: /forums/forum/5
    url(r'^forum/(?P<forum_id>\d+)/?$', views.show_forum, name='show_forum'),
    # ex: /forums/forum/5/add
    url(r'^forum/(?P<forum_id>\d+)/add$', views.add_thread, name='add_thread'),
    # ex: /forums/thread/5
    url(r'^thread/(?P<thread_id>\d+)/?$', views.show_thread, name='show_thread'),
    # ex: /forums/thread/5/add
    url(r'^thread/(?P<thread_id>\d+)/add$', views.add_post, name='add_post'),
    # ex: /forums/post/5
    url(r'^post/(?P<post_id>\d+)/?$', views.show_post, name='show_post'),
    # ex: /forums/post/5/edit
    url(r'^post/(?P<post_id>\d+)/edit$', views.edit_post, name='edit_post'),
)
