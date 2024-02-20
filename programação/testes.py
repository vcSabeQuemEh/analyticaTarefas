import datetime

info_pessoa = {
    'name': "nome sobrenome",
    'birthdate': '2002-07-23',
    'date': 'YYYY-MM-DD'
}

aniversario =datetime.strptime(info_pessoa['birthdate'], '%Y-%m-%d')

hoje = datetime.date.today() 

anos = (hoje - aniversario).years

print(anos)