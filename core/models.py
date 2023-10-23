from django.db import models
from django.contrib.auth.models import User
from django.db import models

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    tipo_de_usuario = models.CharField(max_length=255)

    def __str__(self):
        return self.usuario.username

class Carta(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Rareza(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

class Version(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

class Precio(models.Model):
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    rareza = models.ForeignKey(Rareza, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Precio de {self.carta.nombre} ({self.rareza.nombre}, {self.version.nombre}): ${self.precio}"

    