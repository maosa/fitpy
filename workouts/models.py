from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # import the User model
from django.urls import reverse

# Create workout class (or model)

class Workout(models.Model):
    # no = models.IntegerField() # do not use the no field as Django uses its own ID (primary key)
    date = models.DateField(blank=False, default=timezone.now)
    workout = models.CharField(
        blank=False,
        max_length=50,
        choices=[
            ('Chest', 'Chest'),
            ('Back', 'Back'),
            ('Legs', 'Legs'),
            ('Compound', 'Compound'),
            ('Multisport', 'Multisport'),
            ('Running', 'Running'),
            ('Cycling', 'Cycling'),
            ('Bouldering', 'Bouldering'),
            ('Swimming', 'Swimming'),
            ('Surfing', 'Surfing'),
            ('Skiing', 'Skiing'),
            ('Other', 'Other'),
            ('Rest', 'Rest')
        ] # choices
    ) # CharField
    duration = models.IntegerField(blank=False)
    distance = models.FloatField(blank=True, default=0)
    pace = models.FloatField(blank=True)
    category = models.CharField(blank=True, max_length=50)
    # If a user is deleted, his/her posts are deleted too
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'workout ' + str(self.id) # def __str__(self) must return a string

    # Redirect the user to the detail view of the new workout after the workout has been added
    # Return the URL as a string and let the view handle the redirect for us
    # Alternatively see ~ minute 30
    # https://www.youtube.com/watch?v=-s7e_Fy6NRU&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=10

    def get_absolute_url(self):
        return reverse('workout-detail', kwargs={'pk' : self.pk})
