from django.urls import path
# Create your views here.
from .views import profile, update_profile

urlpatterns = [
  path('<str:username>/',profile, name='profile' ),
  path('<str:username>/update/',update_profile, name='update_profile' ),
]