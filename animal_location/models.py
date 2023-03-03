from django.db import models

class AnimalLocation(models.Model):
    id = models.AutoField(primary_key=True)
    locationPointId = models.ForeignKey('location.Location', on_delete=models.CASCADE)
    dateTimeOfVisitLocationPoint = models.DateTimeField(auto_now_add=True)