from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from .models import Story, Chapter
from .forms import StoryForm, ChapterForm
# Create your views here.

class StoryCreateView(LoginRequiredMixin, CreateView):
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

class ChapterCreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'books/chapter_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.story = get_object_or_404(Story, pk=self.kwargs['story_pk'], author=request.user)
        if not request.user.is_authenticated or request.user != self.story.author:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.story = self.story
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.story.get_absolute_url() or reverse_lazy('story-detail', kwargs={'pk': self.story.pk})
    
class ChapterUpdateView(LoginRequiredMixin, UpdateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'books/chapter_form.html'
    pk_url_kwarg = 'chapter_pk'
    
    def get_queryset(self):
        return Chapter.objects.filter(story__author=self.request.user)
    
    def get_success_url(self):
        return self.chapter.story.get_absolute_url() or reverse_lazy('story-detail', kwargs={'pk': self.chapter.story.pk})
    
class ChapterDetailView(DetailView):
    model               = Chapter
    template_name       = "books/chapter_detail.html"
    context_object_name = "chapter"
    pk_url_kwarg        = "chapter_pk"   # matches URL kwarg

    def get_queryset(self):
       
        return Chapter.objects.select_related("story")    