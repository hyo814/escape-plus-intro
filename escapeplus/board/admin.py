from django.contrib import admin
from .models import Board, Comment, Tag


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'writer', 'created_at', 'view_count')
    list_filter = ('category',)
    search_fields = ('title', 'contents')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('board', 'writer', 'parent', 'created_at')
    list_filter = ('board__category',)
    search_fields = ('content', 'board__title', 'writer__username', 'writer__nickname')
