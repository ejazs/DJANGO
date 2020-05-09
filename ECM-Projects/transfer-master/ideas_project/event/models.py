from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

class Event(models.Model):
  title = models.CharField(max_length=120)
  desc = models.TextField()
  start_date = models.DateField()
  end_date = models.DateField()
  organiser = models.CharField(max_length=120)
  creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  trending_min_likes = models.IntegerField(default=0)
  trending_max_likes = models.IntegerField(default=0)

  trending_min_comments = models.IntegerField(default=0)
  trending_max_comments = models.IntegerField(default=0)

  panel_min_likes = models.IntegerField(default=0)
  panel_min_comments = models.IntegerField(default=0)

  class Meta:
    ordering = ['-created_at']
  def __str__(self):
    return str(self.title)
  
  def get_absolute_url(self):
    return reverse('event:event_detail', kwargs={'id':self.id})

  # validations 
  def clean(self, *args, **kwargs):
    # run the base validation
    super(Event, self).clean(*args, **kwargs)

    # Extra validations for start date and end date
    # if self.start_date < datetime.datetime.now().date():
    #   raise ValidationError('End date cannot be less than today')
    if self.end_date < self.start_date:
      raise ValidationError('End date should be greater than start date.') 
    # Validations for criteria
    if self.trending_min_likes <= 0:
      raise ValidationError('Trending minimum likes should be greater than zero')
    if self.trending_min_comments <= 0:
      raise ValidationError('Trending minimum comments should be greater than zero')


    if self.trending_max_comments< self.trending_min_comments:
      raise ValidationError('Trending max comments cannot be less than trending min')
    if self.trending_max_likes< self.trending_min_likes:
      raise ValidationError('Trending max likes cannot be less than trending min')
    if self.panel_min_comments< self.trending_max_comments:
      raise ValidationError('Panel min comments cannot be less than trending max')
    if self.panel_min_likes< self.trending_max_likes:
      raise ValidationError('Panel min likes cannot be less than trending max')

     

# class Criteria(models.Model):
#   event = models.One(Event, on_delete=models.CASCADE)
#   desc  = models.CharField(max_length=200)
#   fresh = 