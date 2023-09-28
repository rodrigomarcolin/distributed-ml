import pytz
from datetime import datetime, timedelta
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Cliente, Parametro, Resultado, Tarefa
from .serializers import ParametroSerializer, ResultadoSerializer, TarefaSerializer
from django.utils import timezone


class ListaTarefasView(generics.ListAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer


class ResultadosTarefaView(APIView):
    serializer_class = ResultadoSerializer

    def get(self, request, tarefa_id):
        tarefa = Tarefa.objects.get(id=tarefa_id)
        resultados = Resultado.objects.filter(parametro__tarefa=tarefa).all()
        serializer = self.serializer_class(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetalheTarefaView(generics.RetrieveAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer


MAXIMO_PARAMS_POR_ATRIBUICAO = 20


class AtribuirParametrosView(APIView):
    serializer_class = ParametroSerializer

    def post(self, request, tarefa_id):
        # Obter o ID do cliente a partir do corpo da solicitação.
        cliente_key = request.data.get("cliente_key")

        try:
            # Verificar se a tarefa e o cliente existem.
            tarefa = Tarefa.objects.get(id=tarefa_id)
            cliente = Cliente.objects.get(key=cliente_key)

            # Calcular o limite de tempo (4 minutos no passado).
            limite_tempo = timezone.now() - timedelta(minutes=4)

            # Filtrar os parâmetros que atendem aos critérios.
            parametros = Parametro.objects.filter(
                Q(data_atribuicao__lt=limite_tempo) | Q(data_atribuicao__isnull=True),
                tarefa=tarefa,
                resultado_associado__isnull=True,
            ).all()[:MAXIMO_PARAMS_POR_ATRIBUICAO]

            # Atribuir o cliente e atualizar a data de atribuição.
            for parametro in parametros:
                parametro.cliente = cliente
                parametro.data_atribuicao = timezone.now()
                parametro.save()

            # Serializar e retornar a lista de parâmetros.
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


class AtualizarResultadoView(generics.UpdateAPIView):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer

    def post(self, request, tarefa_id):
        try:
            data = request.data.get(
                "resultados"
            )  # Obter a lista de objetos do corpo da solicitação.

            for item in data:
                parametro_id = item.get("parametro_id")
                valor = item.get("valor")

                # Verificar se o parâmetro existe.
                parametro = Parametro.objects.get(id=parametro_id)

                # Verificar se já existe um resultado associado ao parâmetro.
                resultado, created = Resultado.objects.get_or_create(
                    parametro=parametro, valor=valor
                )

                if not created:
                    resultado.valor = valor
                    resultado.save()

            return Response(
                {"detail": "Resultados atualizados com sucesso."},
                status=status.HTTP_200_OK,
            )

        except Parametro.DoesNotExist:
            return Response(
                {"detail": "Parâmetro não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def update(self, request, *args, **kwargs):
        try:
            parametro_id = kwargs["parametro_id"]
            valor = request.data.get("valor")

            # Verificar se o parâmetro existe.
            parametro = Parametro.objects.get(id=parametro_id)

            # Verificar se já existe um resultado associado ao parâmetro.
            resultado, created = Resultado.objects.get_or_create(parametro=parametro)

            # Atualizar o valor do resultado.
            resultado.valor = valor
            resultado.save()

            return Response(
                {"detail": "Resultado atualizado com sucesso."},
                status=status.HTTP_200_OK,
            )

        except Parametro.DoesNotExist:
            return Response(
                {"detail": "Parâmetro não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )


class CriarParametrosView(generics.CreateAPIView):
    serializer_class = ParametroSerializer

    def create(self, request, tarefa_id):
        msg = None
        try:
            tarefa = Tarefa.objects.get(id=tarefa_id)

            data_inicio_str = request.data.get("data_inicio")
            data_fim_str = request.data.get("data_fim")
            formato_data = request.data.get("formato_data")

            data_inicio = datetime.strptime(data_inicio_str, formato_data)
            data_fim = datetime.strptime(data_fim_str, formato_data)

            if data_fim < data_inicio:
                msg = f"A data fim ({data_fim_str}) não pode ser anterior à data de início ({data_inicio_str})"
                raise ValueError(msg)

            parametros_criados = []
            while data_inicio <= data_fim:
                valor_param = {"data": data_inicio.strftime(formato_data)}
                parametro = Parametro(tarefa=tarefa, valor=valor_param)
                parametro.save()
                parametros_criados.append(parametro)
                data_inicio += timedelta(days=1)

            serializer = self.serializer_class(parametros_criados, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Tarefa.DoesNotExist:
            return Response(
                {"detail": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            default_error = "Formato de data inválido."
            return Response(
                {"detail": default_error if msg is None else msg},
                status=status.HTTP_400_BAD_REQUEST,
            )
