from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import EventForm
from .models import Event
from django.utils import timezone
from django.contrib import messages
from ideas_app.models import Idea
from django.db import models
from django.db.models import Avg, Count, Sum
from django.db.models import Q
from itertools import chain
from ideas_app.forms import IdeaForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.
@login_required(login_url='/login/')
def create_idea(request,id):
  event = get_object_or_404(Event, pk=id)
  if event.start_date >timezone.now().date() or event.end_date<timezone.now().date():
    return render(request, 'not_authorized.html',{})
  form = IdeaForm(request.POST or None, initial={'event':event})
  if form.is_valid():
    instance = form.save(commit=False)
    instance.created_by = request.user
    instance.event = event
    instance.save()
    messages.success(request, 'Idea created successfully!!')
    return redirect(reverse('ideas:detail_view', kwargs={'slug':instance.slug}))
  context = {'form': form}
  return render(request, 'create_idea.html', context)


def list_events(request):
  events_list = Event.objects.filter(start_date__lte=timezone.now().date()).filter(end_date__gte=timezone.now().date())
  query = request.GET.get('q')
  print('query',query)
  if query :
    print(' if query',query)
    events_list = events_list.filter(Q(title__icontains=query)|
                                    Q(desc__icontains=query)|
                                    Q(organiser__icontains=query))
  paginator = Paginator(events_list, 5) # Show 10 events per page
  page = request.GET.get('page')
  events = paginator.get_page(page)
  context = {'events':events}
  return render(request, 'active_events.html', context)


def create_event(request):
  if request.user.is_authenticated and request.user.is_staff:
    form = EventForm(request.POST or None)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.creator = request.user
      instance.save()
      return redirect(reverse('event:event_detail', kwargs={'id':instance.id}))
  else:
    return render(request, 'not_authorized.html', {})
  context = {
    'form':form
  }
  return render(request, 'create_event.html',context)

def event_detail(request,id):
  event = get_object_or_404(Event, pk=id)
  context = {
    'event' : event
  }
  return render(request, 'event_detail.html', context)

def update_event(request, id):
  if request.user.is_authenticated and request.user.is_staff:
    event = get_object_or_404(Event, pk=id)
    form = EventForm(request.POST or None, instance = event)
    if form.is_valid():
      form.save()
      messages.success(request, 'Event updated successfully!!')
      return redirect(reverse('event:event_detail', kwargs={'id':event.id}))
  else:
    return render(request, 'not_authorized.html', {})
  context = {'form':form}
  return render(request, 'create_event.html', context)

def delete_event(request, id):
  if request.user.is_authenticated and request.user.is_staff:
    print('here')
    event = get_object_or_404(Event, pk=id)
    if request.POST:
      event.delete()
      messages.success(request, 'Event deleted successfully!!')
    
      return redirect(reverse('event:list_events'))
  else:
    return render(request, 'not_authorized.html', {})
  context = {'event':event}
  return render(request, 'delete_event.html', context)


def event_ideas(request, id):
  event = get_object_or_404(Event, pk=id)
  is_active = True
  if event.start_date > timezone.now().date() or event.end_date < timezone.now().date():
    is_active = False
  like_criteria = event.panel_min_likes
  
  comment_criteria = event.panel_min_comments

  print('like_criteria',like_criteria)
  print('comment_criteria',comment_criteria)
  criteria = {
    'like_criteria' : like_criteria,
    'comment_criteria' : comment_criteria,
    'type' : 'fresh'
  }
  ideas_list = Idea.objects.filter(event=event) 
  query = request.GET.get('q')
  if query:
    ideas_list = ideas_list.filter(
      Q(title__icontains=query) |
      Q(description__icontains=query) |
      Q(created_by__username__icontains=query) 
    )
  paginator = Paginator(ideas_list, 5) # Show 25 contacts per page
  page = request.GET.get('page')
  ideas = paginator.get_page(page)

  context = {'ideas':ideas, 'event':event, 'criteria':criteria, 'is_active':is_active}
  return render(request, 'event_ideas_panel.html',context)

def fresh_event_ideas(request, id):
  event = get_object_or_404(Event, pk=id)
  is_active = True
  if event.start_date > timezone.now().date() or event.end_date < timezone.now().date():
    is_active = False
  like_criteria = event.trending_min_likes
  comment_criteria = event.trending_min_comments
  # print(like_criteria,comment_criteria)
  criteria = {
    'like_criteria' : like_criteria,
    'comment_criteria' : comment_criteria,
    'type' : 'fresh'
  }
  ideas_list = Idea.objects.filter(event=event) 
  query = request.GET.get('q')
  if query:
    ideas_list = ideas_list.filter(
      Q(title__icontains=query) |
      Q(description__icontains=query) |
      Q(created_by__username__icontains=query) 
    )
  paginator = Paginator(ideas_list, 5) # Show 25 contacts per page
  page = request.GET.get('page')
  ideas = paginator.get_page(page)
  # ideas = Idea.objects.annotate(
  #   total_likes=Count('likes'), 
  #   total_comments=Count('comment__comment'),
  #   ).filter(
  #       Q(total_likes__lte=like_criteria) | # this is OR
  #       Q(total_comments__lte=comment_criteria),
  #   )
  context = {'ideas':ideas, 'event':event, 'criteria':criteria,'is_active':is_active}
  return render(request, 'event_ideas.html',context)

def trending_event_ideas(request, id):
  event = get_object_or_404(Event, pk=id)
  is_active = True
  if event.start_date > timezone.now().date() or event.end_date < timezone.now().date():
    is_active = False
  like_min_criteria = event.trending_min_likes
  comment_min_criteria = event.trending_min_comments
  like_max_criteria = event.trending_max_likes
  comment_max_criteria = event.trending_max_comments
  # print(like_min_criteria,comment_min_criteria,like_max_criteria,comment_max_criteria)

  min_likes = Idea.objects.filter(event=event).annotate(
     like_count=models.Count("likes")
    ).filter(like_count__gte=like_min_criteria)

  print('min_likes',min_likes)
  
  min_comments = Idea.objects.filter(event=event).annotate(
     like_count=models.Count("comment")
    ).filter(like_count__gte=comment_min_criteria)

  print('min_comments',min_comments)

  # ideas= Idea.objects.annotate(
  #   total_likes=Count('likes'), 
  #   total_comments=Count('comment__comment'),
  #   ).filter(
  #       Q(total_likes__gte=like_min_criteria) & # this is OR
  #       Q(total_comments__gte=comment_min_criteria),
  #   )
  
 
  
  ideas_list = Idea.objects.filter(event=event) 
  query = request.GET.get('q')
  if query:
    ideas_list = ideas_list.filter(
      Q(title__icontains=query) |
      Q(description__icontains=query) |
      Q(created_by__username__icontains=query) 
    )
  paginator = Paginator(ideas_list, 5) # Show 25 contacts per page
  page = request.GET.get('page')
  ideas = paginator.get_page(page)
  print('final',ideas)

  # print(a)
  criteria = {
    'like_min' : like_min_criteria,
    'comment_min' : comment_min_criteria,
    'like_criteria' : like_max_criteria,
    'comment_criteria' : comment_max_criteria,
    'type' : 'trending'
  }

  context = {'ideas':ideas, 'event':event, 'criteria' :criteria, 'is_active':is_active}
  return render(request, 'event_ideas_trending.html',context)

def featured_event_ideas(request, id):
  event = get_object_or_404(Event, pk=id)
  is_active = True
  if event.start_date > timezone.now().date() or event.end_date < timezone.now().date():
    is_active = False
  like_min_criteria = event.trending_max_likes
  comment_min_criteria = event.trending_max_comments

  like_max_criteria = event.panel_min_likes
  comment_max_criteria = event.panel_min_comments

  min_likes = Idea.objects.filter(event=event).annotate(
     like_count=models.Count("likes")
    ).filter(like_count__gt=like_min_criteria)
  
  min_comments = Idea.objects.filter(event=event).annotate(
     comment_count=models.Count("comment")
    ).filter(comment_count__gt=comment_min_criteria)
  # print('criteria ',like_min_criteria,comment_min_criteria,'yay')
  # print('min_likes',min_likes)
  # print('min_comments',min_comments)
  ideas_list = min_likes & min_comments #and   (max_likes or  max_comments)
  # ideas_list = Idea.objects.filter(event=event) 
  query = request.GET.get('q')
  if query:
    ideas_list = ideas_list.filter(
      Q(title__icontains=query) |
      Q(description__icontains=query) |
      Q(created_by__username__icontains=query) 
    )
  paginator = Paginator(ideas_list, 5) # Show 25 contacts per page
  page = request.GET.get('page')
  ideas = paginator.get_page(page)
  # print('ideas',ideas)
  # print('intersection', min_likes.intersection(min_comments))
  criteria = {
    'like_min' : like_min_criteria,
    'comment_min' : comment_min_criteria,
    'like_criteria' : like_max_criteria,
    'comment_criteria' : comment_max_criteria,
    'type' : 'featured'
  }
  context = {'ideas':ideas, 'event':event, 'criteria' :criteria, 'is_active':is_active}
  return render(request, 'event_ideas_trending_featured.html',context)


@login_required(login_url='/login/')
def past_events(request):
  # if not request.user.is_staff:
  #   return render(request, 'not_authorized.html',{})
  events_list = Event.objects.filter(start_date__lt=timezone.now().date()).filter(end_date__lt=timezone.now().date())
  query = request.GET.get('q')
  if query :
    events_list = events_list.filter(Q(title__icontains=query)|
                                    Q(desc__icontains=query)|
                                    Q(organiser__icontains=query))
  paginator = Paginator(events_list, 5) # Show 10 events per page
  page = request.GET.get('page')
  events = paginator.get_page(page)
  context = {'events':events}
  return render(request, 'past_events.html', context)


@login_required(login_url='/login/')
def upcoming_events(request):
  # if not request.user.is_staff:
  #   return render(request, 'not_authorized.html',{})
  events_list = Event.objects.filter(start_date__gt=timezone.now().date()).filter(end_date__gt=timezone.now().date())
  query = request.GET.get('q')
  if query :
    events_list = events_list.filter(Q(title__icontains=query)|
                                    Q(desc__icontains=query)|
                                    Q(organiser__icontains=query))
  paginator = Paginator(events_list, 5) # Show 10 events per page
  page = request.GET.get('page')
  events = paginator.get_page(page)
  context = {'events':events}
  return render(request, 'upcoming_events.html', context)




# def featured_event_ideas(request, id):
#   event = get_object_or_404(Event, pk=id)
#   like_criteria = event.trending_max_likes
#   comment_criteria = event.trending_max_comments

#   like_max_criteria = event.panel_min_likes
#   comment_max_criteria = event.panel_min_comments

#   ideas = Idea.objects.filter(event=event).annotate(totta_likes=Count('likes')).filter(totta_likes__gt=like_criteria) \
#     .annotate(total_comments=Count('comment__comment')).filter(total_comments__gt=comment_criteria) \
#     .annotate(totta_likes=Count('likes')).filter(totta_likes__lt=like_max_criteria) \
#     .annotate(total_comments=Count('comment__comment')).filter(total_comments__lt=comment_max_criteria)

#   context = {'ideas':ideas, 'event':event}
#   return render(request, 'event_ideas.html',context)


