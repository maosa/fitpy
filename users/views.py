from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # Check that the form is valid
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}') # flashed message
            return redirect('workouts-home')
    else:
        form = UserCreationForm()

    context = {
        'title' : 'Registration form',
        'form' : form
    }

    return render(request, 'users/register.html', context)
