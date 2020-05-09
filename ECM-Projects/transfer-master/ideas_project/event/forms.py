from django import forms
from .models import Event
from pagedown.widgets import PagedownWidget

# Create your tests here.

class EventForm(forms.ModelForm):
  desc = forms.CharField(widget=PagedownWidget())
  start_date =forms.DateField(widget=forms.SelectDateWidget())
  end_date =forms.DateField(widget=forms.SelectDateWidget())
  class Meta:
    model = Event
    fields = ['title','desc','start_date','end_date','organiser','trending_min_likes','trending_max_likes', \
      'trending_min_comments','trending_max_comments', 'panel_min_likes','panel_min_comments']