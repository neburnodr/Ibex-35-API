from django.db import models


# Create your models here.
class Valor(models.Model):
    nombre = models.CharField(max_length=20)
    ultimo = models.FloatField()  # Porcentaje
    variacion_porciento = models.FloatField()  # Porcentaje
    maximo = models.FloatField()
    minimo = models.FloatField()
    volumen = models.IntegerField()
    capitalizacion = models.FloatField()
    actualizacion = models.DateTimeField()

    class Meta:
        verbose_name = 'Valor'
        verbose_name_plural = "Valores"

    def __str__(self):
        return self.nombre
