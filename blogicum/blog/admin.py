from django.contrib import admin

from .models import Category, Comment, Location, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
    )
    list_editable = (
        'category',
        'location',
        'is_published',
    )
    list_filter = (
        'author',
        'location',
        'category',
        'is_published',
    )
    empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'is_published',
    )
    empty_value_display = 'Не задано'


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'is_published',
    )
    empty_value_display = 'Не задано'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
    )
    list_filter = (
        'author',
        'post',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
