from django.contrib import admin
from .models import Ad
from .models import Team

# Register your models here.


class AdAdmin(admin.ModelAdmin):
    list_display = ('sixte_name', 'sixte_location','sixte_prix','sixte_date', 'sixte_limit', 'sixte_link')
    list_filter = ('sixte_name', 'sixte_date')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('ad', 'team_name', 'captain', 'player1', 'player2', 'player3', 'player4', 'player5', 'player6')
    list_filter = ('ad', 'team_name', 'captain')


admin.site.register(Ad, AdAdmin)
admin.site.register(Team, TeamAdmin)
