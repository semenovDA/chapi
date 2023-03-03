from django.db import models
from core.exceptions import *

class Location(models.Model):
  id = models.AutoField(primary_key=True)
  latitude = models.FloatField()
  longitude = models.FloatField()
    
  def validate_unique(self, exclude=None):
    queryset = Location.objects.filter(latitude=self.latitude)
    if(queryset.filter(longitude=self.longitude).exists()):
      raise ConflictExistsException('Point with current latitude and longitude already exists')

  def save(self, *args, **keywords):
    self.validate_unique()
    super(Location, self).save(*args, **keywords)