from django.contrib import admin
from .models import ProfiloUtente

# Register your models here.
@admin.register(ProfiloUtente)
class ProfiloUtenteAdmin(admin.ModelAdmin):
    list_display = ('user', 'numero_tessera', 'data_tesseramento')
    list_filter = ('data_tesseramento',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'numero_tessera')
    readonly_fields = ('numero_tessera', 'data_tesseramento')
