from django.db import models
from django.utils.crypto import get_random_string
import uuid


class Cliente(models.Model):
    key = models.CharField(max_length=40, unique=True, blank=True)
    name = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = get_random_string(length=40)
        super(Cliente, self).save(*args, **kwargs)


class Tarefa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=40, unique=True)
    descricao = models.TextField()
    concluida = models.BooleanField(default=False)
    max_segundos_espera = models.PositiveIntegerField()


class Parametro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tarefa = models.ForeignKey(
        Tarefa, on_delete=models.CASCADE, related_name="parametros"
    )
    cliente = models.ForeignKey(
        "Cliente", on_delete=models.CASCADE, null=True, blank=True
    )
    resultado_associado = models.ForeignKey(
        "Resultado",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parametros",
    )
    data_atribuicao = models.DateTimeField(blank=True, null=True)
    valor = models.JSONField()


class Resultado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parametro = models.OneToOneField(
        Parametro, on_delete=models.CASCADE, related_name="resultado"
    )
    valor = models.JSONField()
