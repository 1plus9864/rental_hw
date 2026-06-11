from django.urls import path
from . import views

urlpatterns = [
    path('', views.house_list, name='house_list'),
    path('create/', views.house_create, name='house_create'),
    path('appointment/<int:house_id>/',views.create_appointment,name='create_appointment'),
    path(
        'house/<int:pk>/edit/',
        views.house_update,
        name='house_update'
    ),

    path(
        'house/<int:pk>/delete/',
        views.house_delete,
        name='house_delete'
    ),
    path('<int:pk>/', views.house_detail, name='house_detail'),
    path('register/', views.register, name='register'),
    path('search/', views.house_search, name='house_search'),
    path(
        'favorite/<int:house_id>/',
        views.toggle_favorite,
        name='toggle_favorite'
    ),
    path(
        'favorites/',
        views.my_favorites,
        name='my_favorites'
    ),
    path(
        'appointments/',
        views.my_appointments,
        name='my_appointments'
    ),
    path(
        'landlord/appointments/',
        views.landlord_appointments,
        name='landlord_appointments'
    ),
    path(
        'my-houses/',
        views.my_houses,
        name='my_houses'
    ),
    
]