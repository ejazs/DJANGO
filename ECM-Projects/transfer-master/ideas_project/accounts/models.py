from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image

# Create your models here.
def user_profile_location(instance,filename):
  return 'profile_pic/{}/{}'.format(instance.user, filename)
class UserProfile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
  description = models.CharField(max_length=180, null=True, blank=True)
  designation = models.CharField(max_length=50, null=True, blank=True)
  education =  models.CharField(max_length=50, null=True, blank=True)
  location =  models.CharField(max_length=50, null=True, blank=True)
  profile_pic = models.ImageField(upload_to=user_profile_location, null=True, blank=True, default='default.jpg')

  def __str__(self):
    return str('profile of {}'.format(self.user))
  
  def save(self, *args, **kwargs):
    super().save(*args,**kwargs)
    img = Image.open(self.profile_pic.path)
    size = (64,64)
    if img.height>64 or img.width>64:
      img.thumbnail(size)
      img.save(self.profile_pic.path)

def create_profile(instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)
    print('Created')
  

post_save.connect(create_profile, sender=User)