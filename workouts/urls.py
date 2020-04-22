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
    path('user/<str:username>/', views.UserWorkoutListView.as_view(), name='user-workouts'),
    # Add a route for specific, individual posts (pk = primary key)
    path('workout/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout-detail'),
    # The CreateView shares a template with the UpdateView; this is expected to be called <model>_form.html
    path('workout/new/', views.WorkoutCreateView.as_view(), name='workout-create'),
    path('workout/<int:pk>/update/', views.WorkoutUpdateView.as_view(), name='workout-update'),
    # A form is used to confirm deletion of a workout - workout_confirm_delete.html
    path('workout/<int:pk>/delete/', views.WorkoutDeleteView.as_view(), name='workout-delete'),
    path('runs/', views.RunListView.as_view(), name='workouts-runs')
]
