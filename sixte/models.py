from django.db import models

# Create your models here.


class Ad(models.Model):
    sixte_name = models.CharField(max_length=40)
    sixte_location = models.CharField(max_length=100)
    sixte_prix = models.IntegerField()
    sixte_date = models.CharField(max_length=11)
    sixte_limit = models.CharField(max_length=11)
    sixte_link = models.URLField()

    class Meta:
        verbose_name = "annonce"
        ordering = ['sixte_date']

    def __str__(self):
        return self.sixte_name

