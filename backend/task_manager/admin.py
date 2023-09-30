from django.contrib import admin
from .models import Cliente, Tarefa, Parametro, Resultado


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
    )
    search_fields = ("name",)


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ("nome", "concluida", "max_segundos_espera", "id")
    list_filter = ("concluida",)
    search_fields = ("nome",)


@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    list_display = (
        "valor",
        "valor_resultado",
        "tarefa",
        "cliente",
        "data_atribuicao",
    )
    list_filter = (
        "tarefa",
        "cliente",
    )
    search_fields = (
        "tarefa__nome",
        "cliente__name",
    )

    def valor_resultado(self, obj: Parametro):
        return str(obj.resultado.valor)

    valor_resultado.short_description = "Resultado"
    valor_resultado.admin_order_field = "resultado__valor"


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ("valor", "parametro", "tarefa_nome")
    list_search = ("valor",)
    list_filter = ("parametro__tarefa",)

    def tarefa_nome(self, obj):
        return obj.parametro.tarefa.nome

    tarefa_nome.short_description = "Tarefa Name"  # Custom column header
    tarefa_nome.admin_order_field = (
        "parametro__tarefa__nome"  # Enable sorting by Tarefa name
    )
