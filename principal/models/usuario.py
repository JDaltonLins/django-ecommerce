from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models

from principal.managers.usuario import UsuarioManager

class Usuario (AbstractUser, PermissionsMixin):
    imagem = models.ImageField(upload_to='usuarios', blank=True)
    moldura = models.ImageField(upload_to='molduras', blank=True)
    color = models.CharField(max_length=6, default='000000')
    pontos = models.IntegerField(default=0)

    objects = UsuarioManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    def __str__(self):
        return self.get_username()