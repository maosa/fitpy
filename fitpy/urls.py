"""fitpy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

# Tell Django which route gets mapped to which url

urlpatterns = [
    path('admin/', admin.site.urls),
    # Link directly to the function that is going to render this from the users application
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    # Create login and logout views (look in users/templates for these templates)
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('workouts.urls')) # workouts app main page
]

# From: https://docs.djangoproject.com/en/3.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
# If we currently are in debug mode, add...

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
