from django.contrib import admin
from .models import Post, Author, Tag, Comments

class PostAdmin(admin.ModelAdmin):
    list_filter = ('author', 'date', 'tags',)  # adding way to filetring in admin pane;
    list_display = ('title', 'date', 'author')  # way of displaying  for conveniency
    prepopulated_fields = {'slug':('title',),}

class CommentsAdmin(admin.ModelAdmin):
    list_filter = ('username', 'text',)  # adding way to filetring in admin pane;
    list_display = ('username', 'text',)

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comments, CommentsAdmin)