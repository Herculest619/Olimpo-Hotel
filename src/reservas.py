# funcão de menu para reservas com as opções de cadastrar, alterar, excluir, listar e voltar
# Como esta declaração o SQL para criar a tabela reserva:
'''
    CREATE TABLE RESERVA 
    ( 
        ID_reserva INT NOT NULL AUTO_INCREMENT,
        Data_check_in_reserva DATE NOT NULL,
        Data_check_out_reserva DATE NOT NULL,
        CLIENTE CHAR(11) NOT NULL,

        PRIMARY KEY (ID_reserva),
        FOREIGN KEY (CLIENTE) REFERENCES CLIENTE (CPF)
            ON UPDATE CASCADE  -- ATUALIZA CPF DO CLIENTE CASO ELE MUDE
            ON DELETE RESTRICT -- NÃO DEIXA DELETAR CLIENTE SE ELE TIVER RESERVA
    );
'''

# Importando as bibliotecas
import os
import utils

# Função de menu para reservas
def menu_reservas(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Menu de reservas')
    print('1 - Cadastrar reserva')
    print('2 - Alterar reserva')
    print('3 - Excluir reserva')
    print('4 - Listar todas as reservas')
    print('5 - Listar reservas por cliente')
    print('6 - Buscar reserva por ID')
    print('7 - Listar reservas por cliente')
    print('8 - Adicionar serviços a uma reserva')
    print('9 - Voltar')
    print('0 - Sair')

    opcao = int(input('\nDigite a opção desejada: '))

    if opcao == 1:
        cadastrar_reserva(cursor, db)
    elif opcao == 2:
        alterar_reserva(cursor, db)
    elif opcao == 3:
        excluir_reserva(cursor, db)
    elif opcao == 4:
        listar_reservas(cursor, db)
    elif opcao == 5:
        listar_reservas_por_cliente(cursor, db)
    elif opcao == 6:
        buscar_reserva_por_id(cursor, db)
    elif opcao == 7:
        listar_reservas_por_cliente(cursor, db)
    elif opcao == 8:
        adicionar_servicos_a_reserva(cursor, db)
    elif opcao == 9:
        from main
        main.menu(cursor, db)
    elif opcao == 0:
        cursor.close()
        exit()
    else:
        print('\nOpção inválida!')
        input('\nPressione enter para continuar...')
        menu_reservas(cursor, db)


# Função cadastrar reserva
def cadastrar_reserva(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela
    print('Cadastrar reserva')

    try: # Tratamento de exceção
        Data_check_in_reserva = input('\nDigite a data de check-in da reserva (AAAA-MM-DD): ')
        if Data_check_in_reserva == "": # Caso o usuário não digite nada
            print('\nData inválida!')
            input('\nPressione enter para continuar...')
            cadastrar_reserva(cursor, db)
        elif not utils.validar_data(Data_check_in_reserva): # Caso a data seja inválida
            print('\nData inválida!')
            input('\nPressione enter para continuar...')
            cadastrar_reserva(cursor, db)
        else:
            Data_check_out_reserva = input('\nDigite a data de check-out da reserva (AAAA-MM-DD): ')
            if Data_check_out_reserva == "": # Caso o usuário não digite nada
                print('\nData inválida!')
                input('\nPressione enter para continuar...')
                cadastrar_reserva(cursor, db)
            elif not utils.validar_data(Data_check_out_reserva): # Caso a data seja inválida
                print('\nData inválida!')
                input('\nPressione enter para continuar...')
                cadastrar_reserva(cursor, db)
            else:
                CPF = input('\nDigite o CPF do cliente (sem pontos ou traços): ')
                if CPF == "": # Caso o usuário não digite nada
                    print('\nCPF inválido!')
                    input('\nPressione enter para continuar...')
                    cadastrar_reserva(cursor, db)
                elif not utils.validar_cpf(CPF): # Caso o CPF seja inválido
                    print('\nCPF inválido!')
                    input('\nPressione enter para continuar...')
                    cadastrar_reserva(cursor, db)
                elif not utils.cpf_existe(cursor, CPF): # Caso o CPF não exista no banco de dados
                    print('\nCPF não cadastrado!')
                    input('\nPressione enter para continuar...')
                    cadastrar_reserva(cursor, db)
                else:
                    numero_quarto = input('\nDigite o número do quarto: ')
                    if numero_quarto == "": # Caso o usuário não digite nada
                        print('\Quarto inválido!')
                        input('\nPressione enter para continuar...')
                        cadastrar_reserva(cursor, db)
                    elif not numero_quarto.isdigit(): # Caso o número seja inválido
                        print('\nQuarto inválido!')
                        input('\nPressione enter para continuar...')
                        cadastrar_reserva(cursor, db)
                    elif not utils.verifica_numero_quarto_existe(cursor, numero_quarto): # Caso o número não exista no banco de dados
                        print('\nQuarto não cadastrado!')
                        input('\nPressione enter para continuar...')
                        cadastrar_reserva(cursor, db)
                    else:
                        cursor.fetchall() # Limpa o cursor
                        #verificar se o quarto está disponível entre as datas de check-in e check-out
                        cursor.execute('SELECT * FROM RESERVA R JOIN ALOCA A ON R.ID_reserva = A.ID_reserva WHERE A.Numero_quarto = %s AND ((R.Data_check_in_reserva <= %s AND R.Data_check_out_reserva >= %s) OR (R.Data_check_in_reserva <= %s AND R.Data_check_out_reserva >= %s))',
                                           (numero_quarto, Data_check_in_reserva, Data_check_in_reserva, Data_check_out_reserva, Data_check_out_reserva))
                        if cursor.fetchone() is not None: # Caso a reserva já exista no banco de dados
                            print('\nQuarto já reservado para esse período!')
                            input('\nPressione enter para continuar...')
                            cursor.fetchall() # Limpa o cursor
                            menu_reservas(cursor, db)
                        else:
                            cursor.fetchall() # Limpa o cursor
                            cursor.execute('INSERT INTO RESERVA (Data_check_in_reserva, Data_check_out_reserva, CLIENTE) VALUES (%s, %s, %s)', 
                                        (Data_check_in_reserva, Data_check_out_reserva, CPF))
                            db.commit() # Salva as alterações

                            cursor.execute('INSERT INTO ALOCA (Numero_quarto, ID_reserva) VALUES (%s, %s)', 
                                           (numero_quarto, cursor.lastrowid)) #cursor.lastrowid pega o ID da reserva que acabou de ser cadastrada
                            db.commit() # Salva as alterações
                            print('\nReserva cadastrada com sucesso!')

    except: # Caso ocorra algum erro
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao cadastrar reserva!')

    input('\nPressione enter para continuar...')
    menu_reservas(cursor, db)


# Função alterar reserva
def alterar_reserva(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela
    print('Alterar reserva')

    try: # Tratamento de exceção
        ID_reserva = input('\nDigite o ID da reserva: ')
        if ID_reserva == "": # Caso o usuário não digite nada
            print('\nID inválido!')
            input('\nPressione enter para continuar...')
            alterar_reserva(cursor, db)
        elif not ID_reserva.isdigit(): # Caso o ID seja inválido
            print('\nID inválido!')
            input('\nPressione enter para continuar...')
            alterar_reserva(cursor, db)
        elif not utils.reserva_existe(cursor, ID_reserva): # Caso o ID não exista no banco de dados
            print('\nID não cadastrado!')
            input('\nPressione enter para continuar...')
            alterar_reserva(cursor, db)
        else:
            cursor.fetchall() # Limpa o cursor
            Data_check_in_reserva = input('\nDigite a nova data de check-in da reserva (AAAA-MM-DD): ')
            if Data_check_in_reserva == "": # Caso o usuário não digite nada
                print('\nData inválida!')
                input('\nPressione enter para continuar...')
                alterar_reserva(cursor, db)
            elif not utils.validar_data(Data_check_in_reserva): # Caso a data seja inválida
                print('\nData inválida!')
                input('\nPressione enter para continuar...')
                alterar_reserva(cursor, db)
            else:
                Data_check_out_reserva = input('\nDigite a nova data de check-out da reserva (AAAA-MM-DD): ')
                if Data_check_out_reserva == "": # Caso o usuário não digite nada
                    print('\nData inválida!')
                    input('\nPressione enter para continuar...')
                    alterar_reserva(cursor, db)
                elif not utils.validar_data(Data_check_out_reserva): # Caso a data seja inválida
                    print('\nData inválida!')
                    input('\nPressione enter para continuar...')
                    alterar_reserva(cursor, db)
                else:
                    CPF = input('\nDigite o novo CPF do cliente (sem pontos ou traços): ')
                    if CPF == "": # Caso o usuário não digite nada
                        print('\nCPF inválido!')
                        input('\nPressione enter para continuar...')
                        alterar_reserva(cursor, db)
                    elif not utils.validar_cpf(CPF): # Caso o CPF seja inválido
                        print('\nCPF inválido!')
                        input('\nPressione enter para continuar...')
                        alterar_reserva(cursor, db)
                    elif not utils.cpf_existe(cursor, CPF): # Caso o CPF não exista no banco de dados
                        print('\nCPF não cadastrado!')
                        input('\nPressione enter para continuar...')
                        alterar_reserva(cursor, db)
                    else:
                        cursor.execute('SELECT * FROM RESERVA WHERE Data_check_in_reserva = %s AND Data_check_out_reserva = %s AND CLIENTE = %s', 
                                       (Data_check_in_reserva, Data_check_out_reserva, CPF))
                        if cursor.fetchone() is not None:
                            print('\nReserva já cadastrada!')
                            input('\nPressione enter para continuar...')
                            cursor.fetchall()
                            alterar_reserva(cursor, db)
                        else:
                            cursor.fetchall()
                            cursor.execute('UPDATE RESERVA SET Data_check_in_reserva = %s, Data_check_out_reserva = %s, CLIENTE = %s WHERE ID_reserva = %s',
                                             (Data_check_in_reserva, Data_check_out_reserva, CPF, ID_reserva))
                            db.commit() # Salva as alterações
                            print('\nReserva alterada com sucesso!')

    except: # Caso ocorra algum erro
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao alterar reserva!')
        
    input('\nPressione enter para continuar...')
    menu_reservas(cursor, db)


# Função excluir reserva
def excluir_reserva(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela
    print('Excluir reserva')

    try: # Tratamento de exceção
        ID_reserva = input('\nDigite o ID da reserva: ')
        if ID_reserva == "": # Caso o usuário não digite nada
            print('\nID inválido!')
            input('\nPressione enter para continuar...')
            excluir_reserva(cursor, db)
        elif not ID_reserva.isdigit(): # Caso o ID seja inválido
            print('\nID inválido!')
            input('\nPressione enter para continuar...')
            excluir_reserva(cursor, db)
        elif not utils.reserva_existe(cursor, ID_reserva): # Caso o ID não exista no banco de dados
            print('\nID não cadastrado!')
            input('\nPressione enter para continuar...')
            excluir_reserva(cursor, db)
        else:
            cursor.fetchall() # Limpa o cursor
            cursor.execute('DELETE FROM RESERVA WHERE ID_reserva = %s', (ID_reserva,)) # Deleta os dados da tabela 
            db.commit() # Salva as alterações
            print('\nReserva excluída com sucesso!')

    except: # Caso ocorra algum erro
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nErro ao excluir reserva!')

    input('\nPressione enter para continuar...')
    menu_reservas(cursor, db)


# Função listar reservas
def listar_reservas(cursor, db):
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela
    print('Listar reservas')
    print('1 - Tabular')
    print('2 - Individual')
    print('9 - Voltar')
    print('0 - Sair')

    opcao = int(input('\nDigite a opção desejada: '))

    if opcao == 1:
        try: # Tratamento de exceção
            cursor.execute('SELECT * FROM RESERVA') # Executa o comando SQL
            print('Listando todas as reservas...\n')
            for linha in cursor.fetchall(): # Imprime todos os dados
                print(linha)

        except: # Caso ocorra algum erro
            print('\nErro ao listar reservas!')

        input('\nPressione enter para continuar...')
        menu_reservas(cursor, db)

    elif opcao == 2:
        try:
            cursor.execute('SELECT * FROM RESERVA') # Executa o comando SQL
            print('Listando todas as reservas...\n')
            for linha in cursor.fetchall():
                utils.imprime_reserva_individual(linha)

        except: