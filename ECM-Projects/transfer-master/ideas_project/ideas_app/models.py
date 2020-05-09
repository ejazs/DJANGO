from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from event.models import Event
# Create your models here.

class Idea(models.Model):
  title = models.CharField(max_length=120)
  description = models.TextField()
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  attachments = models.FileField(blank=True, null=True)
  slug = models.SlugField(max_length=1000,null=True, blank=True)
  category = models.IntegerField(default=0)
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  # comment = models.ForeignKey()

  def __str__(self):
    return str(self.title)
  class Meta:
    ordering = ['-pk']

  def get_absolute_url(self):
    return reverse('ideas:detail_view', kwargs={'slug':self.slug})
  def get_like_api_url(self):
    return reverse('ideas:api_like_toggle', kwargs={'slug':self.slug})
  
  def get_all_comments(self):
    return self.comment_set.all()


def create_slug(instance, created, **kwargs):
  print('in post save')
  if instance.slug is None:
    if created:
      print('created')
      new_slug = slugify(instance.title)
      print('new_slug', new_slug)
      exists = Idea.objects.filter(slug=new_slug).exists()
      
      if exists:
        new_slug = new_slug+str(instance.id)
      instance.slug= new_slug
      instance.save()
  

post_save.connect(create_slug, sender=Idea)