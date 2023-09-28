
## 1

recebe o id de uma tarefa e a chave do cliente
pega um subconjunto de parâmetros da tarefa que satisfaçam as seguintes condições:

1. Não têm resultado associado com valor não nulo
2.  a data de atribuição não existe ou é anterior a 4 minutos no passado

para cada um desses parâmetros:
1. seta o datetime de atribuição como sendo daquele instante
2. seta o cliente atribuido como o id do cliente cuja chave veio na requisição

retorna lista de parametros
<hr>


## 2

endpoint de resultados
recebe requisicao com: id do parametro associado + campo "valor" de um resultado
armazena, no resultado associado ao parametro cujo id foi passado, o valor


## 3

gerador de parâmetros temporais

recebe o id de uma tarefa, uma data de inicio, uma data de fim, e uma string que representa o formato das datas sendo passadas
para cada data nesse intervalo, cria um parametro com o valor da data, associado à tarefa cujo id foi passado


## 4
refatorar e testar views