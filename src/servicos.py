# funcao de menu de servicos com as opcoes de cadastrar servico, alterar servico, excluir servico, listar servicos, buscar e voltar
# Como esta declaração o SQL para criar a tabela servico:
'''
    CREATE TABLE SERVICO 
    ( 
        Nome_servico VARCHAR(100) NOT NULL,
        Valor_servico FLOAT NOT NULL,

        PRIMARY KEY (Nome_servico)
    );
'''

# Importando as bibliotecas
import os
import utils

def menu_servicos(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Menu de serviços')
    print('1 - Cadastrar serviço')
    print('2 - Alterar serviço')
    print('3 - Excluir serviço')
    print('4 - Listar serviços')
    print('5 - Buscar serviço')
    print('9 - Voltar')
    print('0 - Sair')

    opcao = int(input('\nDigite a opção desejada: '))

    if opcao == 1:
        cadastrar_servico(cursor, db)
    elif opcao == 2:
        alterar_servico(cursor, db)
    elif opcao == 3:
        excluir_servico(cursor, db)
    elif opcao == 4:
        listar_servicos(cursor, db)
    elif opcao == 5:
        buscar_servico(cursor, db)
    elif opcao == 9:
        import main
        main.menu(cursor, db)
    elif opcao == 0:
        cursor.close()
        exit()
    else:
        print('Opção inválida!')
        menu_servicos(cursor, db)


# Função cadastrar serviço
def cadastrar_servico(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela
    print('Cadastrar serviço')

    try: # Tratamento de exceção
        Nome_servico = input('\nDigite o nome do serviço: ')
        if Nome_servico == "": # Caso o usuário não digite nada
            cadastrar_servico(cursor, db)
        
        Valor_servico = input('\nDigite o valor do serviço: ')
        if Valor_servico == "": # Caso o usuário não digite nada
            cadastrar_servico(cursor, db)

        if Valor_servico.isnumeric() == False: # Se o valor não for um número
            print('\nValor inválido!')
            input('\nPressione enter para continuar...')
            cadastrar_servico(cursor, db)
        
        if utils.servico_existe_nome(cursor, Nome_servico):
            print('\nServiço já existe!')
            input('\nPressione enter para continuar...')
            menu_servicos(cursor, db)

        cursor.execute('INSERT INTO servico VALUES (%s, %s)', (Nome_servico, Valor_servico)) # Insere os dados na tabela
        db.commit() # Salva as alterações
        print('\nServiço cadastrado com sucesso!')

    except: # Caso ocorra algum erro
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao cadastrar serviço!')

    input('\nPressione enter para continuar...')
    menu_servicos(cursor, db)


# Função alterar serviço
def alterar_servico(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\nAlterar serviço')
    try:
        Nome_servico = input('\nDigite o nome do serviço: ')
        if Nome_servico == "": # Caso o usuário não digite nada
            alterar_servico(cursor, db)
        if not utils.nome_servico_existe(cursor, Nome_servico): # Se o serviço não existir
            print('\nServiço não existe!')
            input('\nPressione enter para continuar...')
            menu_servicos(cursor, db)
        cursor.fetchall() # Limpa o cursor

        Valor_servico = input('\nDigite o valor do serviço: ')
        if Valor_servico == "": # Caso o usuário não digite nada
            print('\nValor inválido!')
            input('\nPressione enter para continuar...')
            alterar_servico(cursor, db)

        cursor.execute('UPDATE servico SET Nome_servico = %s, Valor_servico = %s WHERE Nome_servico = %s', 
                       (Nome_servico, Valor_servico, Nome_servico)) # Altera os dados da tabela
        db.commit() # Salva as alterações
        print('\nServiço alterado com sucesso!')

    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao alterar serviço!')

    input('\nPressione enter para continuar...')
    menu_servicos(cursor, db)


# Função excluir serviço
def excluir_servico(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\nExcluir serviço')
    try:
        Nome_servico = input('\nDigite o nome do serviço: ')
        if Nome_servico == "": # Caso o usuário não digite nada
            excluir_servico(cursor, db)
        if not utils.servico_existe_nome(cursor, Nome_servico): # Se o serviço não existir
            print('\nServiço não existe!')
            input('\nPressione enter para continuar...')
            menu_servicos(cursor, db)
        cursor.fetchall() # Limpa o cursor

        cursor.execute('DELETE FROM servico WHERE Nome_servico = %s', (Nome_servico,)) # Deleta os dados da tabela 
        db.commit() # Salva as alterações
        print('\nServiço excluído com sucesso!')

    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao excluir serviço!')
    
    input('\nPressione enter para continuar...')
    menu_servicos(cursor, db)


# Função listar serviços
def listar_servicos(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Listar todos serviços')
    print('1 - Tabular')
    print('2 - Individuais')
    print('9 - Voltar')
    print('0 - Sair')

    opcao = int(input('\nDigite a opção desejada: '))
    if opcao == 1:
        try:
            cursor.execute('SELECT * FROM servico') # Seleciona todos os dados da tabela
            print('\nListando todos os serviços...')
            for linha in cursor.fetchall(): # Imprime todos os dados
                print(linha) # Imprime todos os dados

        except:
            print('\nErro ao listar serviços!')
        input('\nPressione enter para continuar...')
        menu_servicos(cursor, db)

    elif opcao == 2:
        try:
            cursor.execute('SELECT * FROM servico') # Seleciona todos os dados da tabela
            print('\nListando todos os serviços...')
            for linha in cursor.fetchall(): # Imprime todos os dados
                utils.imprimir_servico_individual(linha) # Imprime todos os dados

        except:
            print('\nErro ao listar serviços!')
        input('\nPressione enter para continuar...')
        menu_servicos(cursor, db)

    elif opcao == 9:
        menu_servicos(cursor, db)

    elif opcao == 0:
        cursor.close()
        exit()

    else:
        print('\nOpção inválida!')
        input('\nPressione enter para continuar...')
        listar_servicos(cursor, db)


# Função buscar serviço
def buscar_servico(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Buscar serviço')
    print('1 - Buscar por nome')
    print('2 - Buscar por valor')  
    print('9 - Voltar')
    print('0 - Sair')

    opcao = int(input('\nDigite a opção desejada: '))
    if opcao == 1:
        try:
            Nome_servico = input('\nDigite o nome do serviço: ')
            if Nome_servico == "": # Caso o usuário não digite nada
                print('\nValor inválido!')
                input('\nPressione enter para continuar...')
                buscar_servico(cursor, db)
            if not utils.servico_existe_nome(cursor, Nome_servico):
                print('\nServiço não existe!')
                input('\nPressione enter para continuar...')
                menu_servicos(cursor, db)
            cursor.fetchall() # Limpa o cursor

            cursor.execute('SELECT * FROM servico WHERE Nome_servico = %s', (Nome_servico,)) # Seleciona todos os dados da tabela
            print('\nListando serviço...')
            for linha in cursor.fetchall(): # Imprime todos os dados
                utils.imprimir_servico_individual(linha)
        
        except:
            print('\nErro ao buscar serviço!')
        input('\nPressione enter para continuar...')
        menu_servicos(cursor, db)

    elif opcao == 2:
        try:
            Valor_servico = input('\nDigite o valor do serviço: ')
            if Valor_servico == "": # Caso o usuário não digite nada
                print('\nValor inválido!')
                input('\nPressione enter para continuar...')
                buscar_servico(cursor, db)
            if not utils.servico_existe_valor(cursor, Valor_servico):
                print('\nServiço não existe!')
                input('\nPressione enter para continuar...')
                menu_servicos(cursor, db)
            cursor.fetchall() # Limpa o cursor

            cursor.execute('SELECT * FROM servico WHERE Valor_servico = %s', (Valor_servico,)) # Seleciona todos os dados da tabela
            print('\nListando serviço...')
            for linha in cursor.fetchall(): # Imprime todos os dados
                utils.imprimir_servico_individual(linha)
        
        except:
            print('\nErro ao buscar serviço!')
        input('\nPressione enter para continuar...')
        menu_servicos(cursor, db)

    elif opcao == 9:
        menu_servicos(cursor, db)

    elif opcao == 0:
        cursor.close()
        exit()

    else:
        print('\nOpção inválida!')
        input('\nPressione enter para continuar...')
        buscar_servico(cursor, db)


