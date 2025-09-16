from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy

# A model to represent different literary genres.
class Genre(models.Model):
  
    name = models.CharField(max_length=100, unique=True, help_text="The name of the genre.")
    slug = models.SlugField(max_length=100, unique=True, blank=True,
                            help_text="A URL-friendly version of the genre name.")
    description = models.TextField(blank=True, help_text="A brief description of the genre.")

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
     
        return self.name

    def get_absolute_url(self):
        
        return reverse('genres:genre-detail', kwargs={'slug': self.slug})

    class Meta:
        # Sets the default ordering for genre lists and the plural name in the admin.
        ordering = ['name']
        verbose_name_plural = "genres"


# A model to represent a story on your website.
class Story(models.Model):
 
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    synopsis = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)


    genres = models.ManyToManyField(Genre, related_name='stories', blank=True, help_text="The genres for this story.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        original_slug = self.slug
        queryset = Story.objects.all()
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)
            
        counter = 1
        while queryset.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('books:story-detail', kwargs={'slug': self.slug})
    
    class Meta:
        # Sets the default ordering for story lists.
        ordering = ['-published_date']

class Chapter(models.Model):
    story = models.ForeignKey(Story, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    chapter_number = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['story','chapter_number']
        unique_together = ('story', 'chapter_number')

    def __str__(self):
        return f"{self.story.title} - Ep. {self.chapter_number}: {self.title}"
    
    def get_success_url(self):
        return reverse_lazy('books:story-detail', kwargs={'slug': self.story.slug})



class ReadingProgressManager(models.Manager):
    def filter_story_first(self, story):
        return self.filter(story=story).first()

class ReadingProgress(models.Model):          # ← ONE class only
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    last_read_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    scroll_position = models.PositiveIntegerField(default=0)
    char_position = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReadingProgressManager()        # ← manager attached here

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'story'],
                name='unique_progress_per_user_story')
        ]
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.story.title} (Last: Ch. {self.last_read_chapter.chapter_number})"