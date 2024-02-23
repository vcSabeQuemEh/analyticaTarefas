#arquivo usado para testes isolados de ferramentas antes de entraren no código principal
#NÃO É UM ARQUIVO IMPORTANTE PARA EXECUÇÃO DO CÓDIGO PRINCIPAL

#deixarei registrado por motivos pessoais mas fique a vontade para analisar


'''import datetime

hoje = datetime.date.today()

ano_hoje = hoje.year
mes_hoje = hoje.month
dia_hoje = hoje.day'''


'''
def calcula_idade(ano_aniversario, mes_aniversario, dia_aniversario,ano_atual,mes_atual,dia_atual):

    idade = ano_hoje - ano_aniversario

    if mes_hoje > mes_aniversario:
        return idade
    elif (mes_hoje == mes_aniversario and dia_hoje >= dia_aniversario):
        return idade
    else:
        return idade - 1
    


info_pessoa = {'name': "nome sobrenome",'aniversario': '2002-07-23','date': 'YYYY-MM-DD'}


ano = int(info_pessoa['aniversario'][:4])
mes = int(info_pessoa['aniversario'][5:7])
dia = int(info_pessoa['aniversario'][8:])


print(ano,mes,dia)
print(ano_hoje,mes_hoje,dia_hoje)




print(calcula_idade(ano,mes,dia,ano_hoje,mes_hoje,dia_hoje))
'''

'''
def verifica_data_futuro(ano_nascimento,mes_nascimento,dia_nascimento , ano, mes, dia):
    #função que verifica se a data é posterior a data de nascimento informada
    data = datetime.date(ano,mes,dia)
    data_nascimento = datetime.date(ano_nascimento, mes_nascimento, dia_nascimento)
    distancia_de_dias = (data - data_nascimento).days

    return distancia_de_dias>0

    


print(verifica_data_futuro(2024,2,20))
'''

'''
d = {
"name": "Lucas Silva",
'birthdate': "2002-07-23",
"date": "2024-07-23"
}
'''

'''def verifica_body_faltando(dicionario):
    #verifica a quantidade minima de elementos no body
    return len(dicionario) < 3
def verifica_body_amais(dicionario):
    return len(dicionario) > 3

print(verifica_body(d))
'''

'''
def verifica_keys(dicionario):
    lista_chaves = list(dicionario.keys())
    lista_valores = list(dicionario.values())
    faltando = []

    if 'name' not in lista_chaves:
        faltando.append('name')
    if 'birthdate' not in lista_chaves:
        faltando.append('birthdate')
    if 'date' not in lista_chaves:
        faltando.append('date')

    return 'faltam os campos: ' + str.join(' ',faltando)

print(verifica_chaves(d))
'''


'''  
import requests

link_municipios = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'

requisicao_municipios = requests.get(link_municipios).json() #requisição do dicionario contendo informações de todos os municipios do brasil
dicionario_nome_id = {} #futuro dicionario nome:id

for municipio in requisicao_municipios: #captura cada municipio do json individualmente

  dicionario_nome_id[municipio["nome"].upper()] = municipio['id'] #utiliza os campos nome e id para incluir em um novo dicionario id:nome (que retorna o id informando o nome do municipio)


id_municipio = dicionario_nome_id['SÃO PAULO']

link_bairros = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{id_municipio}/subdistritos'


requisicao_bairros = requests.get(link_bairros).json()

print(requisicao_bairros)

lista_bairros = []

for bairro in requisicao_bairros:
    lista_bairros.append(bairro["nome"])

resposta = {
    'municipio': 'NOME DO MUNICIPIO',
    'bairros':lista_bairros

    }
print(resposta)

'''