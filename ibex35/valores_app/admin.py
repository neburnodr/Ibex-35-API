from django.contrib import admin
from valores_app.models import Valor


class ValorAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "ultimo",
        "variacion_porciento",
        "maximo",
        "minimo",
        "volumen",
        "capitalizacion",
        "actualizacion",
    )

    ordering = ["-variacion_porciento"]


# Register your models here.
admin.site.register(Valor, ValorAdmin)