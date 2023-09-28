from task_manager.models import Tarefa, Parametro


def insere_parametros_de_data(task_id, parametros):
    tarefa = Tarefa.objects.get(id=task_id)

    for param in parametros:
        valor_param = {"data": param}
        parametro = Parametro(tarefa=tarefa, valor=valor_param)
        parametro.save()
