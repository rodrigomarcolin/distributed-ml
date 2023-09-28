from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('atribuir-parametros/<uuid:tarefa_id>/', AtribuirParametrosView.as_view(), name='atribuir-parametros'),
    path('atualizar-resultado/<uuid:parametro_id>/', AtualizarResultadoView.as_view(), name='atualizar-resultado'),
    path('criar-parametros/<uuid:tarefa_id>/', CriarParametrosView .as_view(), name='criar-parametros'),
]
