from django.db import models

# Create your models here.
class Person(models.Model):
  name = models.CharField(max_length=120)
  desc = models.TextField()
  dob  = models.DateField()

  def __str__(self):
    return str(self.name)