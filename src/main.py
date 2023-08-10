# Função menu principal com as opções de Clientes, reservas, Quartos, serviços e sair
# Cada menu estara em um arquivo separado, com exceção do menu principal
# E ira ter uma integracao com o banco de dados MySQL para armazenar os dados

# Importando as bibliotecas
import os
import mysql.connector

# Connect to database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'barcelona619',
    'database': 'hotel'
}

db = mysql.connector.connect(**db_config)  # Conecta ao banco de dados
cursor = db.cursor()  # Cria um cursor para executar comandos SQL


# Função menu principal com as opções de Clientes, reservas, Quartos, serviços e sair
def menu(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Menu principal')
    print('1 - Clientes')
    print('2 - Reservas')
    print('3 - Quartos')
    print('4 - Serviços')
    print('0 - Sair')
    opcao = int(input('\nDigite a opção desejada: '))

    if opcao == 1:
        import clientes
        clientes.menu_clientes(cursor, db)
    elif opcao == 2:
        import reservas
        reservas.menu_reservas(cursor, db)
    elif opcao == 3:
        import quartos
        quartos.menu_quartos(cursor, db)
    elif opcao == 4:
        import servicos
        servicos.menu_servicos(cursor, db)
    elif opcao == 0:
        cursor.close()  # Fecha o cursor
        exit()
    else:
        print('Opção inválida!')
        menu(cursor, db)


# Executa a função menu
menu(cursor, db)
