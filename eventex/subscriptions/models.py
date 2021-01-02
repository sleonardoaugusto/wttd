import uuid as uuid
from django.db import models

from eventex.subscriptions.validators import validate_cpf


class Subscription(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="nome")
    cpf = models.CharField(max_length=11, validators=[validate_cpf])
    email = models.EmailField(verbose_name="e-mail", blank=True)
    phone = models.CharField(max_length=20, verbose_name="telefone", blank=True)
    paid = models.BooleanField(default=False, verbose_name="pago")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="criado em")

    class Meta:
        verbose_name = "inscrição"
        verbose_name_plural = "inscrições"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
