from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm # import custom-made form (includes email)

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # Check that the form is valid
        if form.is_valid():
            form.save() # save the new user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in!') # flashed message
            # return redirect('workouts-home') # redirect to homepage after user registration
            return redirect('login') # redirect to login page after user registration
    else:
        form = UserRegisterForm()

    context = {
        'title' : 'Registration form',
        'form' : form
    }

    return render(request, 'users/register.html', context)

@login_required # must be logged in to get this functionality (i.e. to view this page)
def profile(request):

    if request.method == 'POST':
        # Create form instances
        # Populate the forms with the User and Profile information
        # Also, pass in the POST data into the forms
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        # Check if both forms are valid before saving them
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # Provide feedback to the user that the forms have been updated
            messages.success(request, f'Your account has been updated!')
            # Redirect the user back to the profile page
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Pass the forms into our template

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)
