from django.db import models

class AnimalType(models.Model):
  id = models.AutoField(primary_key=True)
  type = models.CharField(max_length=255)