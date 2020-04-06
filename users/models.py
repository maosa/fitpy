from django.db import models
from django.contrib.auth.models import User

# Extend the existing User model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 1-to-1 relationship with the User model
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
