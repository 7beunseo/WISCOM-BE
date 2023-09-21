from django.contrib import admin
from .models import Post, Like,Comment, Tag, CommentTag


class CommentInline(admin.TabularInline):
    model=Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','content']
    inlines=[CommentInline]

    def tag_list(self, obj):
        return ','.join([t.name for t in obj.tags.all()])

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Like)

admin.site.register(CommentTag)
