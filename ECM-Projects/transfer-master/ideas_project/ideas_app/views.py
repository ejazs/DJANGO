from django.shortcuts import render, redirect, get_object_or_404
from .forms import IdeaForm
from .models import Idea
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from comment.models import Comment
from comment.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from event.models import Event
from django.utils import timezone
from django.db.models import Q


#Imports for django-rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from notifications.signals import notify

# Create your views here.
# @login_required(login_url='/login/')

def dashboard(request):
  events_list = Event.objects.filter(start_date__lte=timezone.now().date()).filter(end_date__gte=timezone.now().date())
  query = request.GET.get('q')
  if query :
    events_list = events_list.filter(Q(title__icontains=query)|
                                    Q(desc__icontains=query)|
                                    Q(organiser__icontains=query))
  paginator = Paginator(events_list, 5) # Show 10 events per page
  page = request.GET.get('page')
  events = paginator.get_page(page)
  context = {'events':events}
  return render(request, 'active_events.html', context)


def ideas_list(request):
  events_list = Event.objects.filter(start_date__lte=timezone.now().date()).filter(end_date__gte=timezone.now().date())
  # ideas_list = Idea.objects.all()
  # print(ideas_list.count())
  ideas_list = Idea.objects.filter(event__in=events_list)
  query = request.GET.get('q')
  if query:
    ideas_list = ideas_list.filter(
      Q(title__icontains=query)|
      Q(description__icontains=query)|
      Q(created_by__first_name__icontains=query)|
      Q(created_by__last_name__icontains=query)
      )
  # print(ideas_list)
  page = request.GET.get('page', 1)
  paginator = Paginator(ideas_list, 5)
  try:
    ideas = paginator.page(page)
  except PageNotAnInteger:
    ideas = paginator.page(1)
  except EmptyPage:
    ideas = paginator.page(paginator.num_pages)
  context = {'ideas':ideas}
  return render(request, 'ideas_list.html', context)

def detail_view(request, slug):
  idea = get_object_or_404(Idea, slug=slug)
  # print('idea',idea.event.start_date, idea.event.end_date)
  comments_closed = False
  if idea.event.start_date>timezone.now().date() or idea.event.end_date<timezone.now().date():
    comments_closed=True

  comments = Comment.objects.filter(idea=idea).filter(active=True)
  form = CommentForm(request.POST or None)
  if form.is_valid():
    instance = form.save(commit=False)
    instance.user = request.user
    instance.idea = idea
    instance.save()
    if request.user != idea.created_by:
      notify.send(request.user,
              recipient=idea.created_by,
              verb='''<p>{} commented on your idea <a href="{}">{}</a></p> '''
              .format(request.user.first_name+' '+request.user.last_name,
              request.build_absolute_uri(reverse('ideas:detail_view', args=(idea.slug, )))
              ,idea.title))
    return redirect(reverse('ideas:detail_view', kwargs={'slug':idea.slug}))
  context = {'idea':idea, 'comments':comments, 'form':form, 'comments_closed':comments_closed}
  return render(request, 'idea_detail.html',context)

@login_required(login_url='/login/')
def create_idea(request):
  form = IdeaForm(request.POST or None)
  if form.is_valid():
    instance = form.save(commit=False)
    instance.created_by = request.user
    instance.save()
    messages.success(request, 'Idea created successfully!!')
    return redirect('ideas:detail_view', kwargs={'slug':instance.slug})
  context = {'form': form}
  return render(request, 'create_idea.html', context)

@login_required(login_url='/login/')
def update_idea(request, slug):
  idea = get_object_or_404(Idea, slug=slug)
  if request.user==idea.created_by:

    form = IdeaForm(request.POST or None, instance = idea)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
      messages.success(request, 'Idea updated successfully!!')
      return redirect(reverse('ideas:detail_view', kwargs={'slug':idea.slug}))
  else:
    return render(request, 'not_authorized.html',{})
  context = {'form':form}

  return render(request, 'create_idea.html', context)

@login_required(login_url='/login/')
def delete_idea(request, slug):
  idea = get_object_or_404(Idea, slug=slug)
  if request.user == idea.created_by:
    if request.POST:
      idea.delete()
      messages.warning(request, 'Idea deleted successfully!!')
      return redirect('ideas:dashboard')
  else:
    return render(request, 'not_authorized.html',{})

  context = {'idea':idea}
  return render(request, 'delete_idea.html', context)

@login_required(login_url='/login/')
def like(request, slug):
  idea = get_object_or_404(Idea, slug=slug)
  if request.user in idea.likes.all():
    idea.likes.remove(request.user)
  else:
    idea.likes.add(request.user) 
  idea.save()
  return redirect(reverse('ideas:detail_view', kwargs={'slug':idea.slug}))

def login_view(request):
  return render(request, 'login.html', {})

def logout_view(request):
  if 'oauth_token' in request.session:
    del request.session['oauth_token']
  # request.session.delete_test_cookie()
  print('request.session', request.session.items())
  logout(request)
  
  return redirect('https://login.microsoftonline.com/5fa6e0f1-1ac3-459e-9134-64cec6eed94a/oauth2/v2.0/logout?post_logout_redirect_uri=https://172.16.4.155/')

class ApiLikeToggle(APIView):
    """
    View to Toggle like for a Idea.

    * Requires SessionAuthentication authentication.
    * Only Authenticated users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None,slug=None):

        

        """
        Return a list of all users.
        """
        idea = get_object_or_404(Idea, slug=slug)
        updated = False
        liked   = False
        total_likes=0
        if request.user.is_authenticated:
          if request.user not in idea.likes.all():
            idea.likes.add(request.user)
            if request.user != idea.created_by:
              notify.send(request.user,
              recipient=idea.created_by,
              verb='''<p>{} liked your idea <a href="{}">{}</a></p> '''
              .format(request.user.first_name+' '+request.user.last_name,
              request.build_absolute_uri(reverse('ideas:detail_view', args=(idea.slug, )))
              ,idea.title))
            # print(request.build_absolute_uri(reverse('ideas:detail_view', args=(idea.slug, ))))

            updated=True
            liked = True
            total_likes = idea.likes.count()

          else:
            idea.likes.remove(request.user)
            updated=True
            liked = False
            total_likes = idea.likes.count()

        data = {'updated':updated, 'liked':liked, 'total_likes':total_likes}
        return Response(data)

@login_required(login_url='/login/')
def update_comment(request, slug, id):
  idea = get_object_or_404(Idea, slug=slug)
  comment = get_object_or_404(Comment, pk=id)
  if comment.user == request.user:
    comments = Comment.objects.filter(idea=idea)
    form = CommentForm(request.POST or None, instance = comment)
    if form.is_valid():
      form.save()
      messages.success(request, 'comment updated successfully!!')
      return redirect(reverse('ideas:detail_view', kwargs={'slug':idea.slug}))
  else:
    return render(request, 'not_authorized.html',{})
    

  context = {'idea':idea, 'comments':comments, 'form':form, 'comment':comment}
  return render(request, 'idea_detail.html', context)



  
  # form = CommentForm(request.POST or None, instance = comment)
  # if form.is_valid():
  #   form.save()
    
    
  # context = {
  #   'comment' :comment,
  #   'form' : form
  # }

  # return render(request, 'idea_detail.html', context)


@login_required(login_url='/login/')
def delete_comment(request, id):
  comment = get_object_or_404(Comment, pk=id)
  if comment.user==request.user:
    comment_slug = comment.idea.slug
    if request.POST:
      comment.delete()
      messages.success(request, 'Comment delete successfully!!')
      return redirect(reverse('ideas:detail_view', kwargs={'slug':comment_slug}))
  else:
    return render(request, 'not_authorized.html',{})
  context ={'comment':comment}
  return render(request,'delete_comment.html', context)


@login_required(login_url='/login/')
def notifications(request):
  user = request.user
  notifications_list = user.notifications.all()
  paginator = Paginator(notifications_list, 10) # Show 10 notifications per page
  page = request.GET.get('page')
  notifications = paginator.get_page(page)
  notifications_list.mark_all_as_read()
  context = {'notifications':notifications}
  return render(request, 'notifications.html', context)
