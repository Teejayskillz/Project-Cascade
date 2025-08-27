from django import forms 
from .models import Story, Chapter, Genre
from ckeditor.widgets import CKEditorWidget
from django.forms.widgets import CheckboxSelectMultiple

class StoryForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label="Genres"
    )

    class Meta:
        model = Story
        fields = ['title', 'synopsis', 'cover_image', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
           
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['story', 'title', 'content', 'order']
        widgets = {
            'story': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': CKEditorWidget(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['story'].queryset = Story.objects.all()
  