from .views import (CreateTrackingLogAPI, ListTrackingLogAPI, Dashboard,DataListView,
                   PerUserPerAppReportView, PerUserReportView, ListIdleLogAPIView,
                   CreateIdleLogAPIView, IdleDataListView, TestView, test_view)
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'tracking_app'

urlpatterns = [
  path('', Dashboard.as_view(), name='dashboard'),
  path('data/', DataListView.as_view(), name='data'),
  path('idle-data/', IdleDataListView.as_view(), name='idle-data'),
  path('calc-data/', PerUserPerAppReportView.as_view(), name='calc-data'),
  path('per-user/', PerUserReportView.as_view(), name='per-user'),
  path('test/', TestView.as_view(), name='test-user'),

   path('graph/', test_view, name='graph'),

  #Authentication views
  path('login/', LoginView.as_view(template_name= 'login.html'), name='login'),
  path('logout/', LogoutView.as_view(template_name= 'logout.html'), name='logout'),

  #Api views for log
  path('api/v1/list/', ListTrackingLogAPI.as_view(), name='list-api'),
  path('api/v1/create/', CreateTrackingLogAPI.as_view(), name='create-api'),

  #Api views for log
  path('api/v1/idle/', ListIdleLogAPIView.as_view(), name='idle-api'),
  path('api/v1/idle/create/', CreateIdleLogAPIView.as_view(), name='create-api')
]


'''
  
    
http://202.149.220.4:86/api/v1/list   - Lists all data inserted

http://202.149.220.4:86/api/v1/create/   - Inserts new data with request type POST

JSON payload : 
  {
        "app_name": "Demo",
        "app_start_time": "2020-04-15T00:05:00Z",
        "app_end_time": "2020-04-15T00:15:00Z",
        "sys_start_time": "2020-04-15T10:00:00Z",
        "sys_end_time": "2020-04-15T18:00:00Z",
        "username": "LAP 370",
        "emp_id": 10263,
        "status": "YES"
  }


'''