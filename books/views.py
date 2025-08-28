# books/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from .models import Story, Chapter, Genre
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
        return self.request.user == obj.story.author

class StoryManageView(AuthorRequiredMixin, ListView):
    model = Story
    template_name = 'books/story_manage.html'
    context_object_name = 'stories'
    paginate_by = 10

    def get_queryset(self):
        """
        Returns a queryset of Story objects filtered by the current user as the author.
        """
        return Story.objects.filter(author=self.request.user).order_by('-published_date')

class StoryCreateView(AuthorRequiredMixin, CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'books/story_form.html'
    success_url = reverse_lazy('books:story-manage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class StoryListView(LoginRequiredMixin, ListView):
    model = Story
    template_name = 'books/story_list.html'
    context_object_name = 'stories'
    paginate_by = 10
    ordering = ['-published_date']

   
class StoryDetailView(DetailView):
    model = Story
    template_name = 'books/story_detail.html'
    context_object_name = 'story'

class ChapterCreateView(AuthorRequiredMixin, CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'books/chapter_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.story = get_object_or_404(Story, pk=self.kwargs['story_pk'])
        if request.user != self.story.author:
            raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.story = self.story
        return super().form_valid(form)
    
    def get_success_url(self):
        # Correctly passing the story's slug
        return reverse_lazy('books:story-detail', kwargs={'slug': self.story.slug})


class ChapterUpdateView(IsObjectAuthorMixin, UpdateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'books/chapter_form.html'
    pk_url_kwarg = 'chapter_pk'
    
    def get_queryset(self):
        return Chapter.objects.filter(story__author=self.request.user)
    
    def get_success_url(self):
        chapter = self.get_object()
        # Correctly passing the story's slug
        return reverse_lazy('books:story-detail', kwargs={'slug': chapter.story.slug})

class ChapterDetailView(DetailView):
    model               = Chapter
    template_name       = "books/chapter_detail.html"
    context_object_name = "chapter"
    pk_url_kwarg        = "chapter_pk"

    def get_queryset(self):
        return Chapter.objects.select_related("story")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        current_chapter = self.get_object()
        
        # Find the next chapter in the same story with a higher chapter number
        next_chapter = Chapter.objects.filter(
            story=current_chapter.story,
            chapter_number__gt=current_chapter.chapter_number
        ).order_by('chapter_number').first()
        
        # Find the previous chapter with a lower chapter number
        previous_chapter = Chapter.objects.filter(
            story=current_chapter.story,
            chapter_number__lt=current_chapter.chapter_number
        ).order_by('-chapter_number').first()

        # Add the chapters to the context
        context['next_chapter'] = next_chapter
        context['previous_chapter'] = previous_chapter
        
        return context
class StoryDeleteView(AuthorRequiredMixin, IsObjectAuthorMixin, DeleteView):
    model = Story
    template_name = 'books/story_confirm_delete.html'
    success_url = reverse_lazy('books:story-manage')
    context_object_name = 'story'

class ChapterDeleteView(AuthorRequiredMixin, DeleteView):
    model = Chapter
    template_name = 'books/chapter_confirm_delete.html'
    context_object_name = 'chapter'
    pk_url_kwarg = 'chapter_pk'

    def get_queryset(self):
        return Chapter.objects.filter(story__author=self.request.user)

    def get_success_url(self):
        chapter = self.get_object()
        return reverse_lazy('books:story-detail', kwargs={'pk': chapter.story.pk})        
    
def genre_list(request):
    """
    View to list all available genres.
    """
    genres = Genre.objects.all().order_by('name')
    context = {
        'genres': genres
    }
    return render(request, 'books/genre_list.html', context)

def stories_by_genre(request, genre_slug):
    """
    View to list all stories for a specific genre.
    """
    genre = get_object_or_404(Genre, slug=genre_slug)
    stories = Story.objects.filter(genres=genre).order_by('-published_date')
    context = {
        'genre': genre,
        'stories': stories,
    }
    return render(request, 'books/stories_by_genre.html', context)    