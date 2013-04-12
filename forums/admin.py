# Add models to administration screen

from django.contrib import admin
from forums.models import Subforum
from forums.models import Post

class SubforumAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_root_cat', 'parent')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_op', 'subforum', 'content', 'pub_date')

admin.site.register(Subforum, SubforumAdmin)
admin.site.register(Post, PostAdmin)
