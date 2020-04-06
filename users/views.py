from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm # import custom-made form (includes email)

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # Check that the form is valid
        if form.is_valid():
            form.save() # save the new user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}') # flashed message
            return redirect('workouts-home') # redirect to homepage after user registration
    else:
        form = UserRegisterForm()

    context = {
        'title' : 'Registration form',
        'form' : form
    }

    return render(request, 'users/register.html', context)
