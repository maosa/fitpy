from django.urls import path
from .views import (
    WorkoutListView,
    WorkoutDetailView,
    WorkoutCreateView
)
from . import views

# views.home is the home function from views.py
# This returns the HttpResponse

urlpatterns = [
    # path('', views.home, name='workouts-home'),
    path('', WorkoutListView.as_view(), name='workouts-home'), # use class-based views
    # Add a route for specific, individual posts (pk = primary key)
    path('workout/<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
    path('workout/new/', WorkoutCreateView.as_view(), name='workout-create'), # add the create view
    path('runs/', views.runs, name='workouts-runs')
]

#####
