from django.db import models
from django.core.validators import MinValueValidator

class Animal(models.Model):
  # Define choices
  GENDER_CHOICE = [('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')]
  LIFE_STATE_CHOICE = [('ALIVE', 'ALIVE'), ('DEAD', 'DEAD')]

  # Define model fields
  id = models.AutoField(primary_key=True)
  animalTypes = models.ManyToManyField('animal_type.AnimalType')
  weight = models.FloatField(validators=[MinValueValidator(1e-9)])
  length = models.FloatField(validators=[MinValueValidator(1e-9)])
  height = models.FloatField(validators=[MinValueValidator(1e-9)])
  gender = models.CharField(max_length=6, choices=GENDER_CHOICE)
  lifeStatus = models.CharField(max_length=5, choices=LIFE_STATE_CHOICE, default='ALIVE')
  chippingDateTime = models.DateTimeField(auto_now_add=True)
  chipperId = models.ForeignKey('account.Account', on_delete=models.PROTECT)
  chippingLocationId = models.ForeignKey('location.Location', on_delete=models.PROTECT)
  visitedLocations = models.ManyToManyField('animal_location.AnimalLocation', blank=True)
  deathDateTime = models.DateTimeField(null=True, default=None)