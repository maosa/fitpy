from django.urls import path
from . import views

urlpatterns = [
    # views.home is the home function from views.py (this returns the HttpResponse)
    # path('', views.home, name='workouts-home'),
    path('', views.WorkoutListView.as_view(), name='workouts-home'), # use class-based views
    # Add a route for specific, individual posts (pk = primary key)
    path('workout/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout-detail'),
    path('workout/new/', views.WorkoutCreateView.as_view(), name='workout-create'), # add the create view
    path('statistics/', views.statistics, name='workouts-statistics'),
    path('runs/', views.runs, name='workouts-runs')
]
