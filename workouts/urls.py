from django.urls import path
from . import views

# views.home is the home function from views.py
# This returns the HttpResponse

urlpatterns = [
    path('', views.home, name='fitpy-home'),
    path('running/', views.running, name='fitpy-running'),
]

#####
