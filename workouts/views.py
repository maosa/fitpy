from django.shortcuts import render

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]

# Home page

# Create a function to handle the traffic from the home page of the app
# Within the function, return what we want the user to see when they are sent to this route

def home(request):

    context = {
        'posts' : posts,
        'title' : 'TEST'
    }

    return render(request, 'workouts/home.html', context)

# Running page

def running(request):
    return render(request, 'workouts/running.html')

#####
