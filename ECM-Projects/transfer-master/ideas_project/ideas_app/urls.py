from django.urls import path
from .views import dashboard, create_idea, detail_view, update_idea, delete_idea, like, \
                    ApiLikeToggle, login_view, logout_view, update_comment, delete_comment, notifications,ideas_list

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('ideas', ideas_list, name='ideas_list'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('detail/<slug:slug>/', detail_view, name='detail_view'),
    path('detail/<slug:slug>/update/', update_idea, name='update_idea'),
    path('detail/<slug:slug>/delete/', delete_idea, name='delete_idea'),
    # path('create/', create_idea, name='create_idea'),
    path('like/<slug:slug>/', like, name='like'),
    path('like/<slug:slug>/api/',ApiLikeToggle.as_view(), name='api_like_toggle'),
    path('comment/<slug:slug>/update/comment/<int:id>', update_comment, name='update_comment'),
    path('comment/<int:id>/delete/', delete_comment, name='delete_comment'),
    path('notifications/', notifications, name='notifications'),
]
