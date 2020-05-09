from django.db import models
from django.db.models import Sum, Q
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class TrackingLog(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #Will associate user later 
  date = models.DateField(blank=True, null=True, default=timezone.now)    
  app_name = models.CharField(max_length=255) # name of application
  app_start_time = models.DateTimeField()     # application start time
  app_end_time = models.DateTimeField()       # application end time
  app_time_spent = models.DurationField(null=True, blank=True) # Internal field (i will use it for calculations)
  sys_start_time = models.DateTimeField()     # system star time
  sys_end_time =  models.DateTimeField()      # system shutdown time
  username = models.CharField(max_length=255) # Currently it will be system username(assigned to user)
  emp_id = models.IntegerField(blank=True, null=True) # for future reference
  sys_uptime = models.CharField(max_length=120, null=True, blank=True)
  status = models.CharField(max_length=120) # for tracking data status in local DB

  #Added for idle time tracking 4/21/2020
  # idle_start_time = models.DateTimeField(null=True)
  # idle_end_time   = models.DateTimeField(null=True)
  # idle_duration   = models.DurationField(null=True)

  def __str__(self):
    return str(self.username)

  def save(self, **kwargs):
    self.app_time_spent = self.app_end_time - self.app_start_time
    print('self.app_time_spent', self.app_time_spent)
    return super(TrackingLog, self).save(**kwargs)
    
  @property
  def get_idle_time(self):
    return IdleLog.objects.values('date').filter(
      Q(host_id=self.username) and
      Q( date=self.date)
      ).annotate(idle_time= Sum('duration'))

class IdleLog(models.Model):
  username = models.ForeignKey(TrackingLog, on_delete=models.CASCADE, null=True, blank=True)
  host_id  = models.CharField(max_length=255)
  date     = models.DateField()
  start_time = models.DateTimeField()
  end_time   = models.DateTimeField()
  duration  = models.DurationField()

  def save(self, **kwargs):
    self.username = TrackingLog.objects.filter(username = self.host_id).first()
    return super(IdleLog, self).save(**kwargs)

# >>> TrackingLog.objects.values('date', 'app_name', 'app_time_spent').annotate(tcount=Sum('app_time_spent')).filter(app_name='Demo')