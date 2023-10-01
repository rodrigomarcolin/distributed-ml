from rest_framework import serializers
from .models import Cliente, Tarefa, Parametro, Resultado


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"


class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = "__all__"


class ValorParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = ("valor",)


class ResultadoSerializer(serializers.ModelSerializer):
    parametro = ParametroSerializer(required=True)

    class Meta:
        model = Resultado
        fields = "__all__"


class TarefaSerializer(serializers.ModelSerializer):
    parametros = ValorParametroSerializer(many=True, required=False)

    class Meta:
        model = Tarefa
        fields = "__all__"

    def create(self, validated_data):
        parametros_data = validated_data.pop("parametros", [])
        tarefa = Tarefa.objects.create(**validated_data)
        for parametro_data in parametros_data:
            Parametro.objects.create(tarefa=tarefa, **parametro_data)
        return tarefa
