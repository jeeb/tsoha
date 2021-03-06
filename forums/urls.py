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
    # ex: /register
    url(r'^register/?$', views.register, name='register'),
    # ex: forum/add/
    url(r'^forum/add/?$', views.add_forum, name='add_forum'),
    # ex: /forums/forum/5
    url(r'^forum/(?P<forum_id>\d+)/?$', views.show_forum, name='show_forum'),
    # ex: forum/5/edit
    url(r'^forum/(?P<forum_id>\d+)/edit$', views.edit_forum, name='edit_forum'),
    # ex: forum/5/remove
    url(r'^forum/(?P<forum_id>\d+)/remove$', views.remove_forum, name='remove_forum'),
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
    # ex: post/5/remove
    url(r'^post/(?P<post_id>\d+)/remove$', views.remove_post, name='remove_post'),
    # ex: search/
    url(r'^search/?$',  views.search, name='search'),
)
