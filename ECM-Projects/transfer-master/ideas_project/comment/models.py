from django.db import models
from django.conf import settings
from ideas_app.models import Idea
# Create your models here.

class Comment(models.Model):
  comment = models.TextField()
  user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  idea  = models.ForeignKey(Idea, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True)

  def __str__(self):
    return str(self.comment)
  
  class Meta:
    ordering = ['-created_at']

