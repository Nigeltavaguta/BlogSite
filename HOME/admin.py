from django.contrib import admin
from .models import Blog, Category, Comment, Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_guest', 'has_profile_image')
    list_filter = ('is_guest',)
    search_fields = ('name',)
    fields = ('name', 'is_guest', 'profile_image', 'bio')

    def has_profile_image(self, obj):
        return bool(obj.profile_image)
    has_profile_image.boolean = True

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'section', 'status', 'author', 'date')
    list_filter = ('section', 'status', 'category', 'author')
    search_fields = ('title', 'content')
    list_select_related = ('author', 'category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'date')
    list_filter = ('date',)
    search_fields = ('name', 'comment')