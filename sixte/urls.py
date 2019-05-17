from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createad', views.create_ad, name='createad'),
    path('del_ad/<int:id>', views.del_ad, name='del_ad'),
]