import uuid as uuid
from django.db import models


class Subscription(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="nome")
    cpf = models.CharField(max_length=11)
    email = models.EmailField(verbose_name="e-mail")
    phone = models.CharField(max_length=20, verbose_name="telefone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="criado em")

    class Meta:
        verbose_name = "inscrição"
        verbose_name_plural = "inscrições"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
