from django.contrib import admin
from .models import Cliente, Tarefa, Parametro, Resultado

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    search_fields = ('name',)

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'concluida', 'max_segundos_espera', 'id')
    list_filter = ('concluida',)
    search_fields = ('nome',)

@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    list_display = ('tarefa', 'cliente', 'data_atribuicao',)
    list_filter = ('tarefa', 'cliente',)
    search_fields = ('tarefa__nome', 'cliente__name',)
    raw_id_fields = ('resultado_associado',)

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('parametro', 'valor',)
