from django.forms import ModelForm
from django import forms

from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'slug', 'image', 'tags', 'description', 'demo_link', 'source_link']
        labels = {
            'title': 'Name of the project',
            'slug': 'slug',
            'image': 'Scrins of the project',
            'tags': 'tags',
            'description': 'Description of the project',
            'demo_link': 'Demonstration page',
            'source_link': 'Source code from github',
        }
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }
        
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
            
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'review_text']
        labels = {
            'value': 'Estimate this project',
            'review_text': 'Add comment'
        }
        
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})