from django.db import models
from django.contrib.auth.models import User

class Pedidos(models.Model):
    cliente = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    pedido = models.TextField(blank=False)
    enviado = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cliente + ' registrado por ' + self.user.username

class Avatar(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null= True, blank=True)

