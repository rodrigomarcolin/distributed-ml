from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path(
        "atribuir-parametros/<str:nome_tarefa>/",
        AtribuirParametrosView.as_view(),
        name="atribuir-parametros",
    ),
    path(
        "atualizar-resultado/",
        AtualizarResultadoView.as_view(),
        name="atualizar-resultado",
    ),
    path(
        "resultados-tarefa/<str:nome_tarefa>/",
        ResultadosTarefaView.as_view(),
        name="resultados-tarefa",
    ),
    path("tarefa/", TarefasList.as_view(), name="tarefa"),
    path(
        "tarefa/<slug:nome>/",
        TarefaDetailView.as_view(),
        name="detalhes-tarefa",
    ),
]
