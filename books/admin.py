from django.contrib import admin
from .models import Story, Chapter

# Register your models here.
@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
	pass

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
	pass