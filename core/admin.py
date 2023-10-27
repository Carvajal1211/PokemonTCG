from django.contrib import admin
from django.db import models
from core.models import *

admin.site.register(Carta)
admin.site.register(Rareza)
admin.site.register(Version)
admin.site.register(PerfilUsuario)

@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ('carta', 'rareza', 'version', 'code', 'imagen', 'precio', 'fecha_publicacion')
