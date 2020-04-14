from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.CalendarPage.as_view(),name='calendar'),
    path('shift/', views.ShiftRequestView.as_view(), name='shift_request')
]