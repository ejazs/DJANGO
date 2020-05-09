from rest_framework.serializers import ModelSerializer
from .models import TrackingLog, IdleLog

class TrackingLogSerializer(ModelSerializer):
  class Meta:
    model = TrackingLog
    fields = ['date', 'app_name', 'app_start_time', 'app_end_time', 'sys_start_time',
             'sys_end_time', 'username', 'emp_id', 'sys_uptime',  'status']

class IdleLogSerializer(ModelSerializer):
  class Meta:
    model = IdleLog
    fields = ['host_id', 'date', 'start_time', 'end_time', 'duration']