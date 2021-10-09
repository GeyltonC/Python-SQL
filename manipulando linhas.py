# (UPDATE, DELETE e TRUNCATE)

import mysql.connector
import mysql.connector.errors
from time import sleep
from estrutura import *


def exibir_tabela(dados_tabela):
    global cursor
    cursor.execute(f'select * from {dados_tabela};')
    linhas = cursor.fetchall()
    for linha in linhas:
        print(linha)
    sleep(1)


def confirmar_sn(msg):
    msg = f'{msg} [S/N]: '
    while True:
        try:
            opc = input(msg).upper()[0]
            if opc == 'S':
                return True
            elif opc == 'N':
                return False
        except:
            print('Opção Inválida. Tente novamente!')


banco = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='python_youtube'
)
while True:
    tabela = input('Nome da Tabela: ')
    try:
        cursor = banco.cursor()
        atributos_tab = input('Deseja ver os Atributos: [s/n] ').upper()[0]
        atributos = list()
        cursor.execute(f'describe {tabela}')
        rows = cursor.fetchall()
    except:
        print('Erro Para conectar o banco.')
        if not confirmar_sn('Tentar novamente: '):
          quit()
    else:
        break
for row in range(0, cursor.rowcount):
    atributos.append(rows[row][0])
if atributos_tab == 'S':
    print(atributos)
    linha()
while True:
    opc = automenu(['Exibir Tabela', 'Inserir Registros', 'Modificar Registros', 'Deletar Registro',
                    'Deletar Todos os Registros', 'Criar Tabela', 'Apagar Tabela'])
    if opc == 1:
        titulo('Exibir Tabela')
        cursor.execute(f'select * from {tabela}')
        print(f'{tabela} possui {len(cursor.fetchall())} registros')
        exibir_tabela(tabela)
        sleep(1)
    elif opc == 2:
        titulo('Inserir Registro')
        print(f'Preencher na ordem  os atributos: {atributos}')
        while True:
            try:
                cursor.execute(f'select * from {tabela}')
                quant = len(cursor.fetchall())
                valores = {}
                print(f'Total de registros: {quant}')
                for atributo in atributos:
                    a = input(f'{atributo}: ')
                    valores[atributo] = f'{a}'
                data = f'{tuple(valores.values())}'
                print(data)
                cursor.execute(f'insert into {tabela} values {data}')
                opc = input('Novo Registro: [s/n]')
                if opc == 'n':
                    break
            except mysql.connector.Error as erro:
                print('Erro - Banco de dados.')
                print(f'Erro tipo: {erro}')
                break
            except Exception as erro:
                print(f'Erro Tipo. {erro}')
                break
    elif opc == 3:
        sleep(1)
        titulo('Modificar Registro')
        print('Tabela Atual: ')
        exibir_tabela(tabela)
        try:
            chave = input('Informe a chave: ')
            for atributo in atributos:
                mudar = input(f'Deseja mudar o {atributo}? [s/n] ')
                if mudar == 's':
                    mucanca = input(f'Novo {atributo}: ')
                    cursor.execute(f'update {tabela} set {atributo}="{mucanca}" where id = "{chave}"')
        except Exception as erro:
            print(f'ERRO! {erro}')
        banco.commit()
        exibir_tabela(tabela)
    elif opc == 4:
        titulo('Deletar Registro')
        sleep(1)
        try:
            exibir_tabela(tabela)
            condicao = input('Informe o ID para excluir: ')
            if confirmar_sn(f'Deseja Relamente apagar {condicao}'):
                cursor.execute(f'delete from {tabela} where id = {condicao}')
            else:
                print('Ação Cancelada')
        except Exception as erro:
            print(f'Erro. Tipo:{erro}')
    elif opc == 5:
        titulo('Deletar todos os registros')
        sleep(1)
        if confirmar_sn('Realmente deseja apagar todos os registos? '):
            cursor.execute(f'truncate table {tabela}')
    elif opc == 6:
        titulo('Criar Tabela')
        sleep(1)
        nova_tabela = input('Nova tabela: ')
        q_atributos = int(input('Quantidade de atributos: '))
        try:
            comandos = []
            for n in range(0, q_atributos):
                nome_atributo = input('Informe o nome do atributo: ')
                tipo_atributo = input('Informe o tipo do atributo: ')
                extra_atributo = input('Informe o complemento: ')
                if n == q_atributos - 1:
                    f = ''
                else:
                    f = ','
                comando = f'{nome_atributo} {tipo_atributo} {extra_atributo}{f}'
                print(comando)
                linha()
                comandos.append(comando)
            separedor = ' '
            execucao = separedor.join(comandos[:])
            print(execucao)
            comandos.clear()
            cursor.execute(f'create table {nova_tabela} ({execucao})')
        except mysql.connector.Error as erro:
            print(f'Erro: {erro}')
    elif opc == 7:
        titulo('Apagar Tabela')
        cursor.execute('show tables')
        tabelas = cursor.fetchall()
        for tabela in tabelas:
            print(tabela)
        nome_tabela = input('Deseja apagar qual tabela? ')
        try:
            cursor.execute(f'drop table {nome_tabela}')
        except Exception as erro:
            print('Não foi possível apagar pois:', erro)
        else:
            print(nome_tabela, 'Apagado com sucesso')
    else:
        print(f'Resposta inválida.')
    if confirmar_sn('Deseja continuar? '):
        linha()
    else:
        break
'''
Fim!!!
'''