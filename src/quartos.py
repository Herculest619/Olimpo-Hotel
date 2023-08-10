# função de menu de uartos com as de cadastrar, alterar, excluir, listar, voltar e sair
# Como esta declaração o SQL para criar a tabela quartos
'''
    CREATE TABLE QUARTO 
    ( 
        Numero_quarto INT NOT NULL,
        Tipo_quarto VARCHAR(100) NOT NULL,
        Capacidade_quarto INT NOT NULL, 
        Valor_quarto FLOAT NOT NULL,
            
        PRIMARY KEY (Numero_quarto),
    );
'''

import os
import utils


# Função para mostrar o menu de quartos
def menu_quartos(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Menu de Quartos")
    print('1 - Cadastrar quarto')
    print('2 - Alterar quarto')
    print('3 - Excluir quarto')
    print('4 - Listar quartos')
    print('5 - Buscar quarto')
    print('9 - Voltar')
    print('0 - Sair')
    
    opcao = input('\nDigite a opção desejada: ')

    if opcao == '1':
        cadastrar_quarto(cursor, db)
    elif opcao == '2':
        alterar_quarto(cursor, db)
    elif opcao == '3':
        excluir_quarto(cursor, db)
    elif opcao == '4':
        listar_quarto(cursor, db)
    elif opcao == '5':
        buscar_quarto(cursor, db)
    elif opcao == '9':
        import main
        main.menu(cursor, db)
    elif opcao == '0':
        cursor.close()
        exit()
    else:
        print('\nOpção inválida!')
        input('\nPressione enter para continuar...')
        menu_quartos(cursor, db)

# Função para cadastrar um novo quarto
def cadastrar_quarto(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Cadastro de Quartos\n')

    try:
        numero_quarto = input('Número do quarto: ')
        # Verifica se o número do quarto já existe
        if utils.verifica_numero_quarto_existe(cursor, numero_quarto):
            print('\nNúmero de quarto já cadastrado!')
            input('\nPressione enter para continuar...')
            cadastrar_quarto(cursor, db)
        cursor.fetchall() #limpa o cursor

        #verifica se é NULL
        if numero_quarto == '':
            print('\nNúmero de quarto não pode ser nulo!')
            input('\nPressione enter para continuar...')
            cadastrar_quarto(cursor, db)

        #verifica se é inteiro
        if not  numero_quarto.isnumeric():
            print('\nNúmero de quarto deve ser um número inteiro!')
            input('\nPressione enter para continuar...')
            cadastrar_quarto(cursor, db)


        tipo_quarto = input('Tipo do quarto: ')
        #verifica se é NULL
        if tipo_quarto == '':
            print('\nTipo de quarto não pode ser nulo!')
            input('\nPressione enter para continuar...')
            cadastrar_quarto(cursor, db)


        capacidade_quarto = input('Capacidade do quarto: ')
        #verifica se é NULL
        if capacidade_quarto == '':
            print('\nCapacidade de quarto não pode ser nulo!')
            input('\nPressione enter para continuar...')
            cadastrar_quarto(cursor, db)

        #verifica se é inteiro
        if not capacidade_quarto.isnumeric():
            print('\nCapacidade de quarto deve ser um número inteiro!')
            input('\nPressione enter para continuar...')
            cadastrar_quarto(cursor, db)


        valor_quarto = input('Valor do quarto: ')
        #verifica se é NULL
        if valor_quarto == '':
            print('\nValor de quarto não pode ser nulo!')
            input('\nPressione enter para continuar...')
            cadastrar_quarto(cursor, db)

        #verifica se é numero
        if not valor_quarto.isnumeric(): 
            print('\nValor de quarto deve ser um número!')
            input('\nPressione enter para continuar...')
            cadastrar_quarto(cursor, db)
        
        cursor.execute('INSERT INTO QUARTO VALUES (%s, %s, %s, %s)', 
                       (numero_quarto, tipo_quarto, capacidade_quarto, valor_quarto))
        db.commit()
        print('\nQuarto cadastrado com sucesso!')
            
    except:
        #os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao cadastrar quarto!')

    input('\nPressione enter para continuar...')
    menu_quartos(cursor, db)

#função para list um quarto
def listar_quarto(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Lista todos os quartos\n')
    print('1 - Tabular')
    print('2 - Individuais')
    print('9 - Voltar')
    print('0 - Sair')

    opcao = input('\nDigite a opção desejada: ')

    if opcao == '1':
        try:
            cursor.execute('SELECT * FROM QUARTO')
            print('Listando quartos cadastrados...\n')
            for linha in cursor.fetchall(): # fetchall() -> traz todos os registros
                print(linha) # imprime cada registro da tabela em uma linha

        except:
            print('Erro ao listar quartos!')
        input('\nPressione enter para continuar...')
        menu_quartos(cursor, db)

    elif opcao == '2':
        try:
            cursor.execute('SELECT * FROM QUARTO')
            print('Listando quartos cadastrados...\n')
            for linha in cursor.fetchall(): # fetchall() -> traz todos os registros
                utils.imprime_quarto_individual(linha) # imprime cada registro da tabela em uma linha
        
        except:
            print('Erro ao listar quartos!')
        input('\nPressione enter para continuar...')
        menu_quartos(cursor, db)

    elif opcao == '9':
        menu_quartos(cursor, db)

    elif opcao == '0':
        cursor.close()
        exit()

    else:
        print('Opção inválida!')
        input('\nPressione enter para continuar...')
        listar_quarto(cursor, db)

#função para buscar um quarto
def buscar_quarto(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Buscar quarto\n')
    print('1 - Numero')
    print('2 - Tipo')
    print('3 - Capacidade')
    print('9 - Voltar')
    print('0 - Sair')

    opcao = input('\nDigite a opção desejada: ')

    if opcao == '1':
        try:
            numero = input('\nDigite o numero do quarto: ')

            #verifica se o numero existe
            if not utils.verifica_numero_quarto_existe(cursor, numero):
                print('\nNúmero de quarto não existe!')
                input('\nPressione enter para continuar...')
                buscar_quarto(cursor, db)
            cursor.fetchall() #limpa o cursor

            cursor.execute('SELECT * FROM QUARTO WHERE Numero_quarto = %s', (numero,))
            print('\nListando quartos cadastrados...\n')
            for linha in cursor.fetchall(): # fetchall() -> traz todos os registros
                utils.imprime_quarto_individual(linha)

        except:
            print('\nErro ao buscar quarto!')

        input('\nPressione enter para continuar...')
        menu_quartos(cursor, db)

    elif opcao == '2':
        try:
            tipo = input('\nDigite o tipo do quarto: ')

            #verifica se o tipo existe
            if not utils.verifica_tipo_quarto_existe(cursor, tipo):
                print('\nTipo de quarto não existe!')
                input('\nPressione enter para continuar...')
                buscar_quarto(cursor, db)
            cursor.fetchall() #limpa o cursor

            cursor.execute('SELECT * FROM QUARTO WHERE Tipo_quarto = %s', (tipo,))
            print('\nListando quartos cadastrados...\n')
            for linha in cursor.fetchall(): # fetchall() -> traz todos os registros
                utils.imprime_quarto_individual(linha)

        except:
            print('\nErro ao buscar quarto!')
            
        input('\nPressione enter para continuar...')
        menu_quartos(cursor, db)

    elif opcao == '3':
        try:
            capacidade = input('\nDigite a capacidade do quarto: ')

            #verifica se a capacidade existe
            if not utils.verifica_capacidade_quarto_existe(cursor, capacidade):
                print('\nCapacidade de quarto não existe!')
                input('\nPressione enter para continuar...')
                buscar_quarto(cursor, db)
            cursor.fetchall() #limpa o cursor

            cursor.execute('SELECT * FROM QUARTO WHERE Capacidade_quarto = %s', (capacidade,))
            print('\nListando quartos cadastrados...\n')
            for linha in cursor.fetchall(): # fetchall() -> traz todos os registros
                utils.imprime_quarto_individual(linha)

        except:
            print('\nErro ao buscar quarto!')

        input('\nPressione enter para continuar...')
        menu_quartos(cursor, db)

    elif opcao == '9':
        menu_quartos(cursor, db)

    elif opcao == '0':
        cursor.close()
        exit()

    else:
        print('Opção inválida!')
        input('\nPressione enter para continuar...')
        buscar_quarto(cursor, db)

#função para alterar um quarto
def alterar_quarto(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Alterar dados do quarto\n')
    try:
        numero_quarto = input('Digite o numero do quarto: ')

        #verifica se o numero existe
        if not utils.verifica_numero_quarto_existe(cursor, numero_quarto):
            print('Número de quarto não existe!')
            input('\nPressione enter para continuar...')
            menu_quartos(cursor, db)
        cursor.fetchall() #limpa o cursor

        #verifica se é NULL
        if numero_quarto == '':
            print('Número de quarto não pode ser nulo!')
            input('\nPressione enter para continuar...')
            alterar_quarto(cursor, db)

        #verifica se é inteiro
        if not numero_quarto.isdigit():
            print('Número de quarto deve ser um número inteiro!')
            input('\nPressione enter para continuar...')
            alterar_quarto(cursor, db)

        tipo_quarto = input('Tipo do quarto: ')
        #verifica se é NULL
        if tipo_quarto == '':
            print('Tipo de quarto não pode ser nulo!')
            input('\nPressione enter para continuar...')
            alterar_quarto(cursor, db)


        capacidade_quarto = input('Capacidade do quarto: ')
        #verifica se é NULL
        if capacidade_quarto == '':
            print('Capacidade de quarto não pode ser nulo!')
            input('\nPressione enter para continuar...')
            alterar_quarto(cursor, db)

        #verifica se é inteiro
        if not capacidade_quarto.isdigit():
            print('Capacidade de quarto deve ser um número inteiro!')
            input('\nPressione enter para continuar...')
            alterar_quarto(cursor, db)


        valor_quarto = input('Valor do quarto: ')
        #verifica se é NULL
        if valor_quarto == '':
            print('Valor de quarto não pode ser nulo!')
            input('\nPressione enter para continuar...')
            alterar_quarto(cursor, db)

        #verifica se é numero
        if not valor_quarto.isdigit():
            print('Valor de quarto deve ser um número!')
            input('\nPressione enter para continuar...')
            alterar_quarto(cursor, db)

        cursor.execute('UPDATE QUARTO SET Tipo_quarto = %s, Capacidade_quarto = %s, Valor_quarto = %s WHERE Numero_quarto = %s', 
                       (tipo_quarto, capacidade_quarto, valor_quarto, numero_quarto))
        db.commit()
        print('Quarto alterado com sucesso!')

    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Erro ao alterar quarto!')

    input('\nPressione enter para continuar...')
    menu_quartos(cursor, db)


#função para excluir um quarto
def excluir_quarto(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Excluir quarto\n')
    try:
        numero_quarto = input('Digite o numero do quarto: ')

        #verifica se o numero existe
        if not utils.verifica_numero_quarto_existe(cursor, numero_quarto):
            print('\nNúmero de quarto não existe!')
            input('\nPressione enter para continuar...')
            menu_quartos(cursor, db)
        cursor.fetchall() #limpa o cursor

        cursor.execute('DELETE FROM QUARTO WHERE Numero_quarto = %s', (numero_quarto,))
        db.commit()
        print('\n\nQuarto excluído com sucesso!')

    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\nErro ao excluir quarto!')

    input('\nPressione enter para continuar...')
    menu_quartos(cursor, db)

