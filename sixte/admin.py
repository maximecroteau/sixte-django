from django.contrib import admin
from .models import Ad

# Register your models here.

class AdAdmin(admin.ModelAdmin):
   list_display   = ('sixte_name', 'sixte_location','sixte_prix','sixte_date', 'sixte_limit', 'sixte_link')
   list_filter    = ('sixte_name', 'sixte_date')


admin.site.register(Ad, AdAdmin)