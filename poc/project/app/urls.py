from django.urls import path
from .views import PersonCreateView

urlpatterns = [
  path('', PersonCreateView.as_view(),name='create_person'),
]