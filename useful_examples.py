import requests
import json

CHAVE_CLIENTE = ''
codigo_tarefa = ''

url = f"http://127.0.0.1:8000/tasks/atribuir-parametros/{codigo_tarefa}" 

data = {"cliente_key": CHAVE_CLIENTE}

response = requests.post(
    url, data=json.dumps(data), headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    resultado = response.json()
    print("Parâmetros atribuídos com sucesso:", resultado)
elif response.status_code == 404:
    print("Tarefa ou cliente não encontrados.")
else:
    print("Erro desconhecido:", response.status_code, response.text)


# Atualizar resultado

param_id = ''
url = f'http://127.0.0.1:8000/tasks/atualizar-resultado/{param_id}/'

data = [
    {
        'parametro_id': param_id,  
        'valor': 'Novo Valor'
    },
]

response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

if response.status_code == 200:
    print("Resultado atualizado com sucesso.")
elif response.status_code == 404:
    print("Parâmetro não encontrado.")
else:
    print("Erro desconhecido:", response.status_code, response.text)

##Atualizar resultado
tarefa_id = ''
url = f'http://127.0.0.1:8000/tasks/criar-parametros/{tarefa_id}/'

# Dados a serem enviados na solicitação POST
data = {
    'data_inicio': '2013-09-27',
    'data_fim': '2023-09-30',
    'formato_data': '%Y-%m-%d',
}

# Enviar uma solicitação POST para criar os parâmetros
response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

# Verificar a resposta
if response.status_code == 201:
    parametros_criados = response.json()
    print('Parâmetros criados com sucesso:')
    for parametro in parametros_criados:
        print(f'ID: {parametro["id"]}, Valor: {parametro["valor"]}')
elif response.status_code == 404:
    print('Tarefa não encontrada.')
elif response.status_code == 400:
    erro = response.json()
    print(f'Erro: {erro["detail"]}')
else:
    print('Ocorreu um erro inesperado na solicitação.')