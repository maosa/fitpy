from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # import the User model

# Create workout class (or model)

class Workout(models.Model):
    no = models.IntegerField()
    date = models.DateField(default=timezone.now)
    workout = models.CharField(max_length=50)
    duration = models.IntegerField()
    category = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # if a user is deleted, his/her posts are deleted too

    def __str__(self):
        return('workout no: ' + str(self.no)) # def __str__(self) must return a string

# Create running class

# class Run(models.Model):
#     no = models.FloatField()
#     date = models.DateField(default=timezone.now)
#     distance = models.FloatField()
#     duration = models.IntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
