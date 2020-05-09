from django import template
from ..models import Idea
register = template.Library()

@register.simple_tag
def all_ideas_count():
  return Idea.objects.count()

@register.simple_tag
def my_ideas_count(request):
  return Idea.objects.filter(created_by=request.user).count()