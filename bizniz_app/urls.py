from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('twetch/', views.show_images, name='twetch'),
    path('twetch/random/', views.random_images, name='random_images'),
    path('twetch/next/<str:start_index>/', views.next_images, name='next_images'),
    path('previous_images/<int:start_index>/', views.previous_images, name='previous_images'),
]
