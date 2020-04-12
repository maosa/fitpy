from django.urls import path
from . import views
# from .views import (
#     WorkoutListView,
#     WorkoutDetailView,
#     WorkoutCreateView,
#     WorkoutUpdateView
# )

urlpatterns = [
    # views.home is the home function from views.py (this returns the HttpResponse)
    # path('', views.home, name='workouts-home'),
    path('', views.WorkoutListView.as_view(), name='workouts-home'), # use class-based views
    # Add a route for specific, individual posts (pk = primary key)
    path('workout/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout-detail'),
    path('workout/new/', views.WorkoutCreateView.as_view(), name='workout-create'),
    path('workout/<int:pk>/update/', views.WorkoutUpdateView.as_view(), name='workout-update'),
    # A form is used to confirm deletion of a workout - workout_confirm_delete.html
    path('workout/<int:pk>/delete/', views.WorkoutDeleteView.as_view(), name='workout-delete'),
    path('statistics/', views.statistics, name='workouts-statistics'),
    path('runs/', views.runs, name='workouts-runs')
]
