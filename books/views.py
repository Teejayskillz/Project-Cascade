# books/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from .models import Story, Chapter
from .forms import StoryForm, ChapterForm
from django.core.exceptions import PermissionDenied


# A mixin to check if the user is an author
class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
       
        return self.request.user.role == 'author'

# A mixin to check if the user is the author of the object
class IsObjectAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author


class StoryCreateView(AuthorRequiredMixin, CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'books/story_form.html'
    success_url = reverse_lazy('story-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class StoryListView(LoginRequiredMixin, ListView):
    model = Story
    template_name = 'books/story_list.html'
    context_object_name = 'stories'
    paginate_by = 10
    ordering = ['-published_date']

   
class StoryDetailView(LoginRequiredMixin, DetailView):
    model = Story
    template_name = 'books/story_detail.html'
    context_object_name = 'story'

class ChapterCreateView(AuthorRequiredMixin, CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'books/chapter_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        # We now check that the user is an author first with the mixin
        # before checking if they are the author of the specific story.
        self.story = get_object_or_404(Story, pk=self.kwargs['story_pk'])

        # Instead of the manual check, we can raise PermissionDenied
        # if the user is not the author of this specific story.
        if request.user != self.story.author:
            raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.story = self.story
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.story.get_absolute_url() or reverse_lazy('story-detail', kwargs={'pk': self.story.pk})
    
class ChapterUpdateView(IsObjectAuthorMixin, UpdateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'books/chapter_form.html'
    pk_url_kwarg = 'chapter_pk'
    
    def get_queryset(self):
        # This is the correct way to ensure the user can only update their own chapters.
        # This also acts as a security measure, raising a 404 if the object doesn't belong to the user.
        return Chapter.objects.filter(story__author=self.request.user)
    
    def get_success_url(self):
        # Corrected way to get the object and its story
        chapter = self.get_object()
        return reverse_lazy('story-detail', kwargs={'pk': chapter.story.pk})
    
class ChapterDetailView(DetailView):
    model               = Chapter
    template_name       = "books/chapter_detail.html"
    context_object_name = "chapter"
    pk_url_kwarg        = "chapter_pk"   # matches URL kwarg

    def get_queryset(self):
        return Chapter.objects.select_related("story")