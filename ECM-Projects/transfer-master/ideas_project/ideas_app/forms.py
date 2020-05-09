from django import forms
from .models import Idea
from pagedown.widgets import PagedownWidget


class IdeaForm(forms.ModelForm):
  
  description = forms.CharField(widget=PagedownWidget())
  class Meta:
    model  = Idea
    fields = ['title', 'description', 'event'] 