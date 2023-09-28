from rest_framework import serializers
from .models import Cliente, Tarefa, Parametro, Resultado

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = '__all__'

class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = '__all__'

class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = '__all__'
