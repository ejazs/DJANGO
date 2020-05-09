from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile
from .forms import ProfileForm
from django.contrib import messages
from .utils import resize_image
from ideas_app.models import Idea
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def profile(request, username):
  user = get_object_or_404(User, username=username)
  profile = get_object_or_404(UserProfile, user=user)
  total_ideas = Idea.objects.filter(created_by=user).count()
  user_ideas_list = Idea.objects.filter(created_by=user)
  page = request.GET.get('page', 1)
  paginator = Paginator(user_ideas_list, 5)
  try:
    user_ideas = paginator.page(page)
  except PageNotAnInteger:
    user_ideas = paginator.page(1)
  except EmptyPage:
    user_ideas = paginator.page(paginator.num_pages)
  context = {
    'logged_user':user,
    'profile':profile,
    'total_ideas' :total_ideas,
    'user_ideas' : user_ideas
  }
  return render(request, 'profile.html',context)

def update_profile(request, username):
  
  user = get_object_or_404(User, username=username)
  if request.user == user:

    profile = get_object_or_404(UserProfile, user=user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance = profile)
    if form.is_valid():
      form.save()
      messages.success(request, 'Profile updated successfully!!')
      return redirect(reverse('accounts:profile', kwargs={'username': user.username}))
  else:
    return render(request, 'not_authorized.html', {})
  context = {'form':form}
  return render(request, 'update_profile.html', context)
  