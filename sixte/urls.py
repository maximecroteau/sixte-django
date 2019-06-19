from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_ad', views.create_ad, name='create_ad'),
    path('del_ad/<int:id>', views.del_ad, name='del_ad'),
    path('edit_ad/<int:id>', views.edit_ad, name='edit_ad'),
    path('create_team/<int:id>', views.create_team, name='create_team'),
    path('teams/<int:id>', views.view_team, name='view_team'),
    path('del_team/<int:id>', views.del_team, name='del_team'),
    path('edit_team/<int:id>', views.edit_team, name='edit_team'),
    path('my_ad', views.my_ad, name='my_ad'),
    path('my_teams', views.my_teams, name='my_teams'),
    path('signup', views.signup, name='signup'),
    path('friendlist', views.friendlist, name='friendlist'),
    path('askfriend/<int:id>', views.askfriend, name='askfriend'),
    path('addfriend/<int:id>', views.addfriend, name='addfriend'),
    path('refusfriend/<int:id>', views.refusfriend, name='refusfriend'),
    path('searchad', views.searchad, name='searchad'),
    path('searchuser', views.searchuser, name='searchuser'),
    path('unread', views.unread, name='unread')
]