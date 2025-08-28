from django.contrib import admin
from .models import Story, Chapter, Genre


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
  
    list_display = ['title', 'author', 'is_published', 'published_date']
    list_filter = ['is_published', 'published_date', 'genres']
    search_fields = ['title', 'synopsis']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('genres',)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'story', 'chapter_number', 'created_date']
    list_filter = ['story']
    search_fields = ['title', 'content']
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
