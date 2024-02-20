# objetivo - API separada em duas etapas de post e get na qual
# a post - consiste em uma requisição post que retorna uma mensagem amigavel json definida pela equipe-
#  e a post - explicar a post -

# url base - localhost

# endpoints - Post /age
#           - GET /municipio-bairros


# recursos - mensagens


# importações
from flask import Flask, jsonify, request
import datetime

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
        return {'quote':mensagem}
    

    #captura de datas
    hoje = datetime.date.today()

    #separa ano, mes e dia de nascimento do dicionario e converte para int
    ano_nasc = int(info_pessoa['birthdate'][:4])
    mes_nasc = int(info_pessoa['birthdate'][5:7])
    dia_nasc = int(info_pessoa['birthdate'][8:])

    #separa ano, mes e dia informados no dicionario e conserva em string
    #motivo: dias e meses menores que 10 seguirem o modelo dd-mm -> 01/07 pois quando convertidas em int, perde o 0 a esquerda
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
        'quote': "A data informada deverá estar no futuro (de amanhã em diante)" 
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



# encerramento da aplicação
app.run(port=5000, host='localhost', debug=True)
