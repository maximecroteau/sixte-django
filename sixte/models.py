from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Ad(models.Model):
    creator = models.CharField(max_length=25, default="{{ user.username }}")
    sixte_name = models.CharField(max_length=40)
    sixte_location = models.CharField(max_length=100)
    sixte_prix = models.IntegerField()
    sixte_date = models.CharField(max_length=11)
    sixte_limit = models.CharField(max_length=11, blank=True)
    sixte_link = models.URLField(blank=True)

    class Meta:
        verbose_name = "annonce"
        ordering = ['sixte_date']

    def __str__(self):
        return self.sixte_name


class Team(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=30)
    creator = models.CharField(max_length=25, default="{{ user.username }}")
    captain = models.CharField(max_length=25)
    player1 = models.CharField(max_length=25, blank=True)
    player2 = models.CharField(max_length=25, blank=True)
    player3 = models.CharField(max_length=25, blank=True)
    player4 = models.CharField(max_length=25, blank=True)
    player5 = models.CharField(max_length=25, blank=True)
    player6 = models.CharField(max_length=25, blank=True)

    class Meta:
        verbose_name = "equipe"
        ordering = ['ad']

    def __str__(self):
        return self.team_name

