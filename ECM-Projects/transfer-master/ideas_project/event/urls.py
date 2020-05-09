from django.urls import path
from .views import list_events, event_detail, create_event, update_event, delete_event, event_ideas, fresh_event_ideas,\
  trending_event_ideas, featured_event_ideas,create_idea, past_events, upcoming_events
urlpatterns = [
  path('',list_events, name ='list_events'),
  path('past_events/',past_events, name ='past_events'),
  path('upcoming_events/',upcoming_events, name ='upcoming_events'),
  path('event/create/',create_event, name ='create_event'),
  path('event/<int:id>/',event_detail, name ='event_detail'),
  path('event/<int:id>/create_idea/',create_idea, name ='create_idea'),
  path('event/<int:id>/update/',update_event, name ='update_event'),
  path('event/<int:id>/ideas/',event_ideas, name ='event_ideas'),
  path('event/<int:id>/ideas/fresh/',fresh_event_ideas, name ='fresh_event_ideas'),
  path('event/<int:id>/ideas/trending/',trending_event_ideas, name ='trending_event_ideas'),
  path('event/<int:id>/ideas/featured/',featured_event_ideas, name ='featured_event_ideas'),
  path('event/<int:id>/delete/',delete_event, name ='delete_event'),
  
]