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
    order = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['story','order']
        unique_together = ('story', 'order')

    def __str__(self):
        return f"{self.story.title} - Ep. {self.order}: {self.title}"
    
    def get_success_url(self):
        return reverse_lazy('books:story-detail', kwargs={'slug': self.story.slug})

