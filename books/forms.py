from django import forms 
from .models import Story, Chapter
from ckeditor.widgets import CKEditorWidget

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'synopsis', 'cover_image']
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
        # You can also add classes here if needed for more complex logic
        # For example: self.fields['title'].widget.attrs.update({'class': 'form-control'})