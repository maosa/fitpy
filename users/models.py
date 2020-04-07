from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Extend the existing User model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 1-to-1 relationship with the User model
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Override the save method to scale down user profile pictures

    def save(self):
        super().save() # run the save method of the parent class
        # Resize the image using the Pillow library/package
        img = Image.open(self.image.path) # open the image of the current instance
        # Re-size if the image's height or width is greater than 300 pixels
        if img.height > 300 or img.width > 300:
            output_size = (300, 300) # define maximum image size
            img.thumbnail(output_size) # re-size
            img.save(self.image.path) # save to the same path to override the large image
