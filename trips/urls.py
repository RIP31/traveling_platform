from django.urls import path
from . import views

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('<int:pk>/', views.trip_detail, name='trip_detail'),
    path('<int:pk>/book/', views.booking_trip, name='booking_trip'),
    path('search/', views.search_trips, name='search_trips'),
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/trip/create/', views.create_trip, name='create_trip'),
    path('provider/trip/<int:pk>/edit/', views.edit_trip, name='edit_trip'),
    path('provider/trip/<int:pk>/delete/', views.delete_trip, name='delete_trip'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
]
