from django.urls import path, include
from . import views

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('signup/',views.signup_view, name='signup'),
    path('profile/', views.user_profile_view, name='profile')
]