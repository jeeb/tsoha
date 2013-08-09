# Add models to administration screen
from django.contrib import admin

# Forums-specific models under here
from forums.models import Subforum
from forums.models import Thread
from forums.models import Post

class SubforumAdmin(admin.ModelAdmin):
    list_display = ('parent', 'title', 'description', 'is_root_cat')

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('subforum', 'title', 'creator', 'sticky', 'creation_date')

class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'title', 'content', 'poster', 'pub_date')

admin.site.register(Subforum, SubforumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
