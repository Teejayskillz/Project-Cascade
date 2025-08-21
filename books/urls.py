# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # STORY
    path("stories/", views.StoryListView.as_view(), name="story-list"),
    path("stories/create/", views.StoryCreateView.as_view(), name="story-create"),
    path("stories/<slug:slug>/", views.StoryDetailView.as_view(), name="story-detail"),

    # CHAPTER
    path(
        "stories/<int:story_pk>/chapters/add/",
        views.ChapterCreateView.as_view(),
        name="chapter-add"
    ),
    path(
        "stories/<int:story_pk>/chapters/<int:chapter_pk>/edit/",
        views.ChapterUpdateView.as_view(),
        name="chapter-edit"
    ),

    path(
    "stories/<int:story_pk>/chapters/<int:chapter_pk>/",
    views.ChapterDetailView.as_view(),
    name="chapter-detail"
),
]