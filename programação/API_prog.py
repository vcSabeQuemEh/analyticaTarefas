# objetivo - API separada em duas etapas de post e get na qual
# a post - consiste em uma requisição post que retorna uma mensagem amigavel json definida pela equipe-
#  e a get - requisião GET que recebe uma informação query de municipio e retorna os bairros pertencentes ao municipio -

# url base - http://localhost:5000/

# endpoints - Post /age  body{'name':'nome' , 'birthdate' : 'yyyy-mm-dd' , 'date': 'YYYY-MM-DD'}
                             
#           - GET /municipio-bairros (?municipio=NOME-DO-MUNICIPIO)


# recursos - mensagens


# importações
from flask import Flask, jsonify, request
import datetime
import requests

# criação da aplicação
app = Flask(__name__)

#primeira tarefa
#____________________________________________________________________________________________________________
def verifica_data_futuro(ano, mes, dia):
    '''função que verifica se a data informada é futura ao dia de hoje
        retorna verdadeiro caso seja futura e falso caso contrário
        int,int,int -> bool'''
    data = datetime.date(ano,mes,dia)
    hoje = datetime.date.today()
    distancia_de_dias = (data - hoje).days

    return distancia_de_dias>0

def verifica_body_faltando(dicionario):
    ''' verifica se atingiu a quantidade minima de elementos no body'''
    return len(dicionario) < 3

# def verifica_body_amais(dicionario):
#     ''' verifica se ultrapassou a quantidade maxima de elementos no body'''
#     return len(dicionario) > 3

def verifica_keys(dicionario):
    '''verifica se as chaves requisitadas constam na requisição'''
    lista_chaves = list(dicionario.keys())
    faltando = []

    if 'name' not in lista_chaves:
        faltando.append('name')
    if 'birthdate' not in lista_chaves:
        faltando.append('birthdate')
    if 'date' not in lista_chaves:
        faltando.append('date')

    return 'faltam o(os) campo(os): ' + str.join(' ',faltando)
    

def calcula_idade(ano_nascimento, mes_nascimento, dia_nascimento, ano_atual, mes_atual, dia_atual):
    '''função que recebe uma data de nascimento e uma data futura e calcula a quantidade de anos passados entre essas duas datas
        int,int,int,int,int,int -> int'''
    idade = ano_atual - ano_nascimento

    if mes_atual > mes_nascimento:
        return idade
    elif (mes_atual == mes_nascimento and dia_atual >= dia_nascimento):
        return idade
    else:
        return idade - 1
   

@app.route("/age", methods=['POST'])
def geraMensagem():
    info_pessoa = request.get_json()

    #verificações body
    faltando = verifica_body_faltando(info_pessoa)
    #sobrando = verifica_body_amais(info_pessoa)

    #encerra antes de fazer os calculos sem as informações
    if faltando:
        mensagem = "há falta de informações no body " + verifica_keys(info_pessoa)
        return {'erro':mensagem}
    

    #captura de datas
    hoje = datetime.date.today()

    #separa ano, mes e dia de nascimento do dicionario e converte para int
    ano_nasc = int(info_pessoa['birthdate'][:4])
    mes_nasc = int(info_pessoa['birthdate'][5:7])
    dia_nasc = int(info_pessoa['birthdate'][8:])

    #separa ano, mes e dia informados no dicionario e conserva em string
    #motivo: dias e meses menores que 10 seguirem o modelo dd-mm -> 01/07 pois quando convertidas em int, perde o 0 a esquerda
    #2002-12-23
    ano_info_str = info_pessoa['date'][:4]
    mes_info_str = info_pessoa['date'][5:7]
    dia_info_str = info_pessoa['date'][8:]
    #separa ano, mes e dia informados no dicionario e converte para int
    ano_info = int(info_pessoa['date'][:4])
    mes_info = int(info_pessoa['date'][5:7])
    dia_info = int(info_pessoa['date'][8:])

    #verificações data
    futuro = verifica_data_futuro(ano_info, mes_info,dia_info)
    
    #mensagem de erro detalhado
    erroFuturo = {
        'erro': "A data informada deverá estar no futuro (de amanhã em diante)" 
    }

    #calculos
    idadeHoje = calcula_idade(ano_nasc, mes_nasc, dia_nasc, hoje.year, hoje.month, hoje.day)
    idadeFutura = calcula_idade(ano_nasc ,mes_nasc ,dia_nasc ,ano_info ,mes_info ,dia_info )


    #monta menssagem
    mensagem = f"Olá,{info_pessoa['name']}! Você tem anos {idadeHoje} anos e em {dia_info_str +'/'+mes_info_str+"/"+ano_info_str} você terá {idadeFutura} anos"

    #retorno
    resposta = {
        'quote': mensagem,
        'ageNow': idadeHoje,
        'ageThen': idadeFutura
    }

    #resultado da função de calcular se a 'date' está no futuro ou não, caso não esteja retorna mensagem de erro
    if futuro:
        return jsonify(resposta)
    else:
        return jsonify(erroFuturo)
#_________________________________________________________________________________________________________________________________________________________________________
#segunda tarefa
@app.route("/municipio-bairros", methods=['GET'])
def bairros_por_municipio():
    #requisição e tratamento de entrada
    municipio_nome = request.args.get('municipio',None,None) #capura o municipio informado no query
    municipio_nome = municipio_nome.replace('-'," ") #coloca espaço entre as palavras
    municipio_nome = municipio_nome.upper()          #coloca todas as letras em maiusculo

    
    #requsição dos municipios na API do IBGE e indexação em um dicionario {nome:id}
    link_municipios = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'

    requisicao_municipios = requests.get(link_municipios).json() #requisição do dicionario contendo informações de todos os municipios do brasil
    dicionario_nome_id = {} #futuro dicionario {nome:id}

    for municipio in requisicao_municipios: #captura cada municipio do json individualmente

        dicionario_nome_id[municipio["nome"].upper()] = municipio['id'] #utiliza os campos nome e id para incluir em um novo dicionario id:nome (que retorna o id informando o nome do municipio)

    #verificação se o municipio informado existe na listagem de municipios do brasil, caso não esteja retorna erro
    if municipio_nome not in list(dicionario_nome_id.keys()):
        mensagem = {
            'erro' : 'Municipio não encontrado, digite um Municipio válido'
        }
        return mensagem


    #busca o id do municipio infordado no query
    id_municipio = dicionario_nome_id[municipio_nome]

    #requisição dos bairros do municipio informado
    link_bairros = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{id_municipio}/subdistritos'
    requisicao_bairros = requests.get(link_bairros).json() ##requisição do dicionario contendo informações de todos os bairros do municipio informado

    #no caso de não haver subsdistritos busca os distritos
    if requisicao_bairros == []: #uma requisição vazia retorna lista vazia ao inves de dicionario vazio
        link_bairros = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{id_municipio}/distritos'
        requisicao_bairros = requests.get(link_bairros).json() 


    lista_bairros = [] #futura lista de nomes dos bairros

    #pega cada bairro individualmente da lista de bairros fornecida pela API no IBGE
    for bairro in requisicao_bairros:
        lista_bairros.append(bairro["nome"]) #capura o nome de cada um e adiciona na lista de nomes de bairros

    #dicionario da resposta esperada pela tarefa
    resposta = {
        'municipio': municipio_nome,
        'bairros':lista_bairros

        }
    return jsonify(resposta)

# encerramento da aplicação
app.run(port=5000, host='localhost', debug=True)
