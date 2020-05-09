from django.contrib import admin
from .models import TrackingLog, IdleLog
# Register your models here.

admin.site.register(TrackingLog)
admin.site.register(IdleLog)