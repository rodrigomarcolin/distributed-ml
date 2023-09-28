from rest_framework import generics
from .models import Resultado, Tarefa
from .serializers import ResultadoSerializer, TarefaSerializer


class ListaTarefasView(generics.ListAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer


class ResultadosTarefaView(generics.ListAPIView):
    serializer_class = ResultadoSerializer

    def get_queryset(self):
        tarefa_id = self.kwargs['tarefa_id']
        return Resultado.objects.filter(parametro__tarefa_id=tarefa_id)

class DetalheTarefaView(generics.RetrieveAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer