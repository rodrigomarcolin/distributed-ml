from django.utils.crypto import get_random_string
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
import uuid


class Cliente(models.Model):
    key = models.CharField(max_length=40, unique=True, blank=True)
    name = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_authenticated = True

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = get_random_string(length=40)
        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tarefa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=40, unique=True)
    descricao = models.TextField()
    concluida = models.BooleanField(default=False)
    max_segundos_espera = models.PositiveIntegerField()

    def __str__(self):
        return self.nome


class ParametroQueryset(models.QuerySet):
    def available_by_task_id(self, task_id: str, maximum_dt_attr: datetime):
        return self.filter(
            Q(data_atribuicao__lt=maximum_dt_attr) | Q(data_atribuicao__isnull=True),
            Q(resultado__isnull=True) | Q(resultado__valor__isnull=True),
            tarefa__id=task_id,
        )

    def available_by_task_name(self, task_id: str, maximum_dt_attr: datetime):
        return self.filter(
            Q(data_atribuicao__lt=maximum_dt_attr) | Q(data_atribuicao__isnull=True),
            Q(resultado__isnull=True) | Q(resultado__valor__isnull=True),
            tarefa__nome=task_id,
        )

    def create_or_update_resultados(self, param_id_to_resultado_valor_map):
        with transaction.atomic():
            for (
                parametro_id,
                valor_resultado,
            ) in param_id_to_resultado_valor_map.items():
                parametro = Parametro.objects.get(id=parametro_id)

                # Create or update the associated Resultado object
                resultado, created = Resultado.objects.get_or_create(
                    parametro=parametro, defaults={"valor": valor_resultado}
                )

                # If not created, update the valor
                if not created:
                    resultado.valor = valor_resultado
                    resultado.save()

    def bulk_set_client_by_key(self, parametros, cliente_key):
        with transaction.atomic():
            for param in parametros:
                param.atribui_cliente(cliente_key)


class Parametro(models.Model):
    objects = ParametroQueryset.as_manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tarefa = models.ForeignKey(
        Tarefa, on_delete=models.CASCADE, related_name="parametros"
    )
    cliente = models.ForeignKey(
        "Cliente", on_delete=models.CASCADE, null=True, blank=True
    )
    data_atribuicao = models.DateTimeField(blank=True, null=True)
    valor = models.JSONField()

    def atribui_cliente(self, cliente_key: str):
        self.cliente = Cliente.objects.get(key=cliente_key)
        self.data_atribuicao = timezone.now()
        self.save()

    def __str__(self):
        return str(self.valor)


class ResultadoQueryset(models.QuerySet):
    def by_tarefa_id(self, tarefa_id):
        return self.filter(parametro__tarefa_id=tarefa_id)

    def by_tarefa_nome(self, tarefa_name: str):
        return self.filter(parametro__tarefa__nome=tarefa_name)


class Resultado(models.Model):
    objects = ResultadoQueryset.as_manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parametro = models.OneToOneField(
        Parametro, on_delete=models.CASCADE, related_name="resultado"
    )
    valor = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.valor)
