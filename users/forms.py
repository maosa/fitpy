from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create a new form that inherits from UserCreationForm

class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    # Specify the model we want this form to interact with
    # Meta gives us a nested namespace for configurations and keeps the configurations in one place
    # Within the configuration we are saying that the model that will be affected in the User model
    # i.e. form.save() will save to the User model
    # This also includes the fields to be displayed and in what order

    class Meta:
        model = User # whenever the form validates, it's going to create a new user
        # Fields to be displayed in the registration form (in the order they will appear)
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
