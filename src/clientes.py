# função de menu de clientes com as opções de cadastrar, alterar, excluir, listar e voltar
# Como esta declaração o SQL para criar a tabela clientes:
'''
    CREATE TABLE CLIENTE 
    ( 
        CPF CHAR(11) NOT NULL,
        Nome_cliente VARCHAR(100) NOT NULL,  
        Telefone_cliente VARCHAR(20),  
        Endereco_cliente VARCHAR(200),
        Data_nasc_cliente DATE NOT NULL,
        CPF_TITULAR CHAR(11),

        PRIMARY KEY (CPF),
        FOREIGN KEY (CPF_TITULAR) REFERENCES CLIENTE (CPF)
            ON UPDATE CASCADE  -- ATUALIZA CPF DO ACOMPANHANTE CASO ELE MUDE
            ON DELETE SET NULL -- DELETA ACOMPANHANTE CASO CLIENTE SEJA DELETADO
    );
'''

# Importando as bibliotecas
import os
import utils

# Função de menu de clientes
def menu_clientes(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Menu clientes')
    print('1 - Cadastar cliente')
    print('2 - Alterar cliente')
    print('3 - Excluir cliente')
    print('4 - Listar clientes')
    print('5 - Buscar cliente')
    print('9 - Voltar')
    print('0 - Sair')
    
    opcao = int(input('\nDigite a opção desejada: '))

    if opcao == 1:
        cadastrar_cliente(cursor, db)
    elif opcao == 2:
        alterar_cliente(cursor, db)
    elif opcao == 3:
        excluir_cliente(cursor, db)
    elif opcao == 4:
        listar_cliente(cursor, db)
    elif opcao == 5:
        buscar_cliente(cursor, db)
    elif opcao == 9:
        import main
        main.menu(cursor, db)
    elif opcao == 0:
        cursor.close()
        exit()
    else:
        print('Opção inválida!')
        input('\nPressione enter para continuar...')
        menu_clientes(cursor, db)

# Função cadastrar cliente
def cadastrar_cliente(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Cadastrar cliente')
    try:
        CPF = input('\nDigite o CPF do cliente (sem pontos ou traços): ')
        if not utils.validar_cpf(CPF):  # Se o CPF não for válido
            print('\nCPF inválido!')  # Imprime uma mensagem de erro
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            cadastrar_cliente(cursor, db)

        # Se o CPF já existir no banco de dados
        if utils.cpf_existe(cursor, CPF): # Se o CPF já existir no banco de dados
            print('\nCPF já cadastrado!')  # Imprime uma mensagem de erro
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            cadastrar_cliente(cursor, db)
        cursor.fetchall() #limpa o cursor

        Nome_cliente = input('\nDigite o nome do cliente: ')
        if Nome_cliente == "": # Se o nome for vazio
            cadastrar_cliente(cursor, db) # Retorna ao menu de cadastro de cliente

        Telefone_cliente = input('\nDigite o telefone do cliente: ')

        Endereco_cliente = input('\nDigite o endereço do cliente: ')

        Data_nasc_cliente = input('\nDigite a data de nascimento do cliente (AAAA-MM-DD): ')
        # Se a data de nascimento não for válida
        if not utils.validar_data(Data_nasc_cliente):
            # Imprime uma mensagem de erro
            print('\nData de nascimento inválida!')
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            cadastrar_cliente(cursor, db)

        if Data_nasc_cliente == "":  # Se a data de nascimento for vazia
            # Imprime uma mensagem de erro
            print('\nData de nascimento inválida!')
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            cadastrar_cliente(cursor, db)

        CPF_TITULAR = input(
            '\nDigite o CPF do titular caso o cliente seja um acompanhante (sem pontos ou traços): ')
        if CPF_TITULAR == "":  # Se o CPF do titular for vazio
            CPF_TITULAR = None  # CPF_TITULAR recebe NULL
        if CPF_TITULAR and not utils.cpf_existe(cursor, CPF_TITULAR): # Se o CPF do titular não existir no banco de dados
            print('\nCPF do titular não existe!')
            input('\nPressione enter para continuar...')
            cadastrar_cliente(cursor, db)
        cursor.fetchall() #limpa o cursor

        cursor.execute('INSERT INTO cliente (CPF, Nome_cliente, Telefone_cliente, Endereco_cliente, Data_nasc_cliente, CPF_TITULAR) VALUES (%s, %s, %s, %s, %s, %s)',
                       (CPF, Nome_cliente, Telefone_cliente, Endereco_cliente, Data_nasc_cliente, CPF_TITULAR))  # Executa o comando SQL
        db.commit()  # Salva as alterações no banco de dados
        print('\nCliente cadastrado com sucesso!')
    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao cadastrar cliente!')

    input('\nPressione enter para continuar...')
    menu_clientes(cursor, db)

# Função listar todos os clientes
def listar_cliente(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Listar todos clientes')
    print('1 - Tabular')
    print('2 - Individuais')
    print('9 - Voltar')
    print('0 - Sair')

    opcao = int(input('\nDigite a opção desejada: '))
    if opcao == 1:
        try:
            cursor.execute('SELECT * FROM cliente')  # Executa o comando SQL
            # Imprime uma mensagem de status
            print('\nListando clientes cadastrados...')
            for linha in cursor.fetchall():  # Itera sobre o resultado
                print(linha)  # imprime a linha completa

        except:
            print('\nErro ao listar clientes!')
        input('\nPressione enter para continuar...')
        menu_clientes(cursor, db)  # Retorna ao menu de clientes

    elif opcao == 2:
        try:
            cursor.execute('SELECT * FROM cliente')  # Executa o comando SQL
            # Imprime uma mensagem de status
            print('\nListando clientes cadastrados...')
            for linha in cursor.fetchall():  # Itera sobre o resultado
                # Imprime cada cliente em uma nova linha
                utils.imprimir_cliente_individual(linha)
        except:
            print('\nErro ao listar clientes!')
        input('\nPressione enter para continuar...')
        menu_clientes(cursor, db)  # Retorna ao menu de clientes

    elif opcao == 9:
        menu_clientes(cursor, db)

    elif opcao == 0:
        cursor.close()
        exit()
    else:
        print('Opção inválida!')
        input('\nPressione enter para continuar...')
        listar_cliente(cursor, db)

# Função buscar cliente
def buscar_cliente(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Buscar cliente')
    print('1 - CPF')
    print('2 - Nome')
    print('9 - Voltar')
    print('0 - Sair')

    opcao = int(input('\nDigite a opção desejada: '))
    if opcao == 1:
        try:
            CPF = input('\nDigite o CPF do cliente (sem pontos ou traços): ')
            if not utils.validar_cpf(CPF):  # Se o CPF não for válido
                print('\nCPF inválido!')  # Imprime uma mensagem de erro
                # Pausa a execução do programa
                input('\nPressione enter para continuar...')
                # Retorna ao menu de cadastro de cliente
                buscar_cliente(cursor, db)

            # Se o CPF não existir no banco de dados
            if not utils.cpf_existe(cursor, CPF): # Se o CPF não existir no banco de dados
                print('\nCPF não cadastrado!')  # Imprime uma mensagem de erro
                # Pausa a execução do programa
                input('\nPressione enter para continuar...')
                # Retorna ao menu de cadastro de cliente
                buscar_cliente(cursor, db)
            cursor.fetchall() #limpa o cursor

            cursor.execute('SELECT * FROM cliente WHERE CPF = %s', (CPF,))  # Executa o comando SQL
            # Imprime uma mensagem de status
            print('\nListando cliente cadastrado...')
            for linha in cursor.fetchall():  # Itera sobre o resultado
                # Imprime cada cliente em uma nova linha
                utils.imprimir_cliente_individual(linha)

        except:
            print('\nErro ao listar clientes!')
        input('\nPressione enter para continuar...')
        menu_clientes(cursor, db)  # Retorna ao menu de clientes

    elif opcao == 2:
        try:
            Nome_cliente = input('\nDigite o nome do cliente: ')

            #testar se o nome existe no banco de dados
            if not utils.nome_cliente_existe(cursor, Nome_cliente): # Se o nome não existir no banco de dados
                print('\nNome não cadastrado!')  # Imprime uma mensagem de erro
                buscar_cliente(cursor, db)
            cursor.fetchall() #limpa o cursor

            cursor.execute('SELECT * FROM cliente WHERE Nome_cliente = %s', (Nome_cliente,))  # Executa o comando SQL
            # Imprime uma mensagem de status
            print('\nListando cliente cadastrado...')
            for linha in cursor.fetchall():  # Itera sobre o resultado
                # Imprime cada cliente em uma nova linha
                utils.imprimir_cliente_individual(linha)
        except:
            print('\nErro ao listar clientes!')
        input('\nPressione enter para continuar...')
        menu_clientes(cursor, db)  # Retorna ao menu de clientes

    elif opcao == 9:
        menu_clientes(cursor, db)

    elif opcao == 0:
        cursor.close()
        exit()

    else:
        print('Opção inválida!')
        input('\nPressione enter para continuar...')
        buscar_cliente(cursor, db)

# Função alterar cliente
def alterar_cliente(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Alterar dados cliente')
    try:
        CPF = input('\nDigite o CPF do cliente (sem pontos ou traços): ')
        if not utils.validar_cpf(CPF):  # Se o CPF não for válido
            print('\nCPF inválido!')  # Imprime uma mensagem de erro
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            alterar_cliente(cursor, db)

        # Se o CPF não existir no banco de dados
        if not utils.cpf_existe(cursor, CPF): # Se o CPF não existir no banco de dados
            print('\nCPF não cadastrado!')  # Imprime uma mensagem de erro
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            alterar_cliente(cursor, db)
        cursor.fetchall() #limpa o cursor

        Nome_cliente = input('\nDigite o nome do cliente: ')

        Telefone_cliente = input('\nDigite o telefone do cliente: ')

        Endereco_cliente = input('\nDigite o endereço do cliente: ')

        Data_nasc_cliente = input('\nDigite a data de nascimento do cliente (AAAA-MM-DD): ')
        # Se a data de nascimento não for válida
        if not utils.validar_data(Data_nasc_cliente):
            # Imprime uma mensagem de erro
            print('\nData de nascimento inválida!')
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            alterar_cliente(cursor, db)

        if Data_nasc_cliente == "":  # Se a data de nascimento for vazia
            # Imprime uma mensagem de erro
            print('\nData de nascimento inválida!')
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            alterar_cliente(cursor, db)

        CPF_TITULAR = input(
            '\nDigite o CPF do titular caso o cliente seja um acompanhante (sem pontos ou traços): ')
        if CPF_TITULAR == "":  # Se o CPF do titular for vazio
            CPF_TITULAR = None  # CPF_TITULAR recebe NULL
        if CPF_TITULAR and not utils.cpf_existe(cursor, CPF_TITULAR):
            print('\nCPF do titular não existe!')
            input('\nPressione enter para continuar...')
            alterar_cliente(cursor, db)
        cursor.fetchall() #limpa o cursor

        cursor.execute('UPDATE cliente SET CPF = %s, Nome_cliente = %s, Telefone_cliente = %s, Endereco_cliente = %s, Data_nasc_cliente = %s, CPF_TITULAR = %s WHERE CPF = %s', 
                       (CPF, Nome_cliente, Telefone_cliente, Endereco_cliente, Data_nasc_cliente, CPF_TITULAR, CPF))  # Executa o comando SQL
        db.commit()  # Salva as alterações no banco de dados
        print('\nCliente alterado com sucesso!')

    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao alterar cliente!')

    input('\nPressione enter para continuar...')
    menu_clientes(cursor, db)

# Função excluir cliente
def excluir_cliente(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Excluir cliente')
    try:
        CPF = input('\nDigite o CPF do cliente (sem pontos ou traços): ')
        if not utils.validar_cpf(CPF):  # Se o CPF não for válido
            print('\nCPF inválido!')  # Imprime uma mensagem de erro
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            menu_clientes(cursor, db)

        # Se o CPF não existir no banco de dados
        if not utils.cpf_existe(cursor, CPF): # Se o CPF não existir no banco de dados
            print('\nCPF não cadastrado!')  # Imprime uma mensagem de erro
            # Pausa a execução do programa
            input('\nPressione enter para continuar...')
            # Retorna ao menu de cadastro de cliente
            menu_clientes(cursor, db)
        cursor.fetchall() #limpa o cursor

        cursor.execute('DELETE FROM cliente WHERE CPF = %s', (CPF,))  # Executa o comando SQL
        db.commit()  # Salva as alterações no banco de dados
        print('\nCliente excluído com sucesso!')

    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao excluir cliente!')

    input('\nPressione enter para continuar...')
    menu_clientes(cursor, db)

