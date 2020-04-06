from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# post_save is a signal that is fired after an object (i.e. a User) is created/saved
# In this case, User is the sender i.e. this is what is sending the signal
# A receiver is a function that gets the signal and then performs some task
# In this case, the function will create a Profile

# Automatically create a Profile when a User registers/signs up

# The function below will run every time a User is created

@receiver(post_save, sender=User) # when a User is saved, send the post_save signal that is received by the receiver
def create_profile(sender, instance, created, **kwargs): # create_profile function is the receiver
    # The arguments above are passed to the function by the post_save signal
    # If the User was created, then create a Profile object for that User
    if created:
        Profile.objects.create(user=instance)

# Define a function to save the profile every time the User object gets saved
# i.e. create and save User, create Profile, save Profile

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs): # **kwargs accepts any additional arguments at the end of the function
    instance.profile.save()
