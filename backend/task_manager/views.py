from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .authentication import BearerTokenAuthentication
from .models import Cliente, Parametro, Resultado, Tarefa
from .serializers import ParametroSerializer, ResultadoSerializer, TarefaSerializer


class TarefasList(generics.ListCreateAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]


class TarefaDetailView(RetrieveAPIView):
    queryset = Tarefa.objects.all()
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TarefaSerializer
    lookup_field = "nome"


class ResultadosTarefaView(APIView):
    serializer_class = ResultadoSerializer

    def get(self, request, nome_tarefa):
        resultados = Resultado.objects.by_tarefa_nome(nome_tarefa)
        serialized_resultados = self.serializer_class(resultados, many=True).data
        return Response(serialized_resultados, status=status.HTTP_200_OK)


class DetalheTarefaView(generics.RetrieveAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer


class AtribuirParametrosView(APIView):
    """
    Pega parâmetros disponíveis de uma determinada tarefa
    e os atribui ao cliente que fez a solicitação
    """

    serializer_class = ParametroSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    default_batch_size = 20

    def post(self, request: Request, nome_tarefa: str):
        cliente_key = request.auth

        batch_size = int(
            request.query_params.get("batch_size", self.default_batch_size)
        )

        try:
            max_segundos = Tarefa.objects.get(nome=nome_tarefa).max_segundos_espera
            max_dt_attr = timezone.now() - timedelta(seconds=max_segundos)

            parametros = Parametro.objects.available_by_task_name(
                nome_tarefa, max_dt_attr
            )[:batch_size]
            Parametro.objects.bulk_set_client_by_key(parametros, cliente_key)

            serializer = self.serializer_class(parametros, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Tarefa.DoesNotExist:
            return Response(
                {"detail": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND
            )
        except Cliente.DoesNotExist:
            return Response(
                {"detail": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )


class AtualizarResultadoView(APIView):
    """
    Atualiza os resultados associados a determinados parâmetros
    """

    authentication_classes = [BearerTokenAuthentication]
    serializer_class = ResultadoSerializer

    def post(self, request):
        try:
            data = request.data.get("resultados")
            parametro_valor_map = {
                item.get("parametro_id"): item.get("valor") for item in data
            }

            Parametro.objects.create_or_update_resultados(parametro_valor_map)

            return Response(
                {"detail": "Resultados atualizados com sucesso."},
                status=status.HTTP_200_OK,
            )

        except Parametro.DoesNotExist:
            return Response(
                {"detail": "Um ou mais parâmetros não foram encontrados."},
                status=status.HTTP_404_NOT_FOUND,
            )
