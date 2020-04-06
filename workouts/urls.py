from django.urls import path
from . import views

# views.home is the home function from views.py
# This returns the HttpResponse

urlpatterns = [
    path('', views.home, name='workouts-home'),
    path('runs/', views.runs, name='workouts-runs'),
    path('register/', views.runs, name='workouts-register'),
]

#####
