from django.conf.urls import patterns, url

from forums import views

urlpatterns = patterns('',
    # ex: /forums/
    url(r'^$', views.index, name='index'),
    # ex: /forums/forum/5
    url(r'^forum/(?P<forum_id>\d+)$', views.show_forum, name='show_forum'),
    # ex: /forums/thread/5
    url(r'^thread/(?P<thread_id>\d+)$', views.show_thread, name='show_thread'),
    # ex: /forums/post/5
    url(r'^post/(?P<post_id>\d+)$', views.show_post, name='show_post'),
    # ex: /forums/post/add
    url(r'^post/add$', views.add_post, name='add_post'),
    # ex: /forums/post/5/edit
    url(r'^post/(?P<post_id>\d+)/edit$', views.edit_post, name='edit_post'),
)
