from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_ad', views.create_ad, name='create_ad'),
    path('del_ad/<int:id>', views.del_ad, name='del_ad'),
    path('edit_ad/<int:id>', views.edit_ad, name='edit_ad'),
]