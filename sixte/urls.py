from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createad', views.create_ad, name='createad')
]