from datetime import datetime

# Função validar CPF se tem 11 digitos, se não tem letras e se não tem caracteres especiais
def validar_cpf(cpf):
    if len(cpf) != 11:
        return False
    elif not cpf.isnumeric(): # Se não for numérico
        return False
    elif not cpf.isdigit(): # Se não for dígito
        return False
    else:
        return True

# Função verificar se o CPF existe no banco de dados
def cpf_existe(cursor, cpf):
    cursor.execute('SELECT CPF FROM cliente WHERE CPF = %s', (cpf,)) # Executa o comando SQL
    return cursor.fetchone() is not None # Retorna True se o CPF existir no banco de dados

# Função validar data
def validar_data(data):
    try:
        datetime.strptime(str(data), '%Y-%m-%d')  # Converte o objeto datetime.date para string e depois faz a conversão
        return True
    except ValueError:
        return False
    
# Função para imprimir os dados do cliente de forma individual
def imprimir_cliente_individual(linha):
    print("CPF: ", linha[0]) # Imprime cada coluna em uma nova linha, [] indica a coluna
    print("Nome: ", linha[1]) 
    print("Telefone: ", linha[2])
    print("Endereço: ", linha[3])
    print("Data de nascimento: ", linha[4])
    print("CPF do titular: ", linha[5])
    print("\n")

#função veicar se o numero do quarto já existe
def verifica_numero_quarto_existe(cursor, numero_quarto):
    cursor.execute('SELECT Numero_quarto FROM QUARTO WHERE Numero_quarto = %s', (numero_quarto,))
    return cursor.fetchone() is not None

def imprimir_servico_individual(linha):
    print("Nome do serviço: ", linha[0]) # Imprime cada coluna em uma nova linha, [] indica a coluna
    print("Valor do serviço: ", linha[1])
    print("\n")

# Função para verificar se o serviço existe no banco de dados
def nome_servico_existe(cursor, Nome_servico):
    cursor.execute('SELECT Nome_servico FROM servico WHERE Nome_servico = %s', (Nome_servico,)) # Executa o comando SQL
    return cursor.fetchone() is not None # Retorna True se o serviço existir no banco de dados

# Função para verificar se o serviço existe no banco de dados
def servico_existe_valor(cursor, Valor_servico):
    cursor.execute('SELECT Valor_servico FROM servico WHERE Valor_servico = %s', (Valor_servico,)) # Executa o comando SQL
    return cursor.fetchone() is not None # Retorna True se o serviço existir no banco de dados

# Função para verificar se o serviço existe no banco de dados
def servico_existe_nome(cursor, Nome_servico):
    cursor.execute('SELECT Nome_servico FROM servico WHERE Nome_servico = %s', (Nome_servico,)) # Executa o comando SQL
    return cursor.fetchone() is not None # Retorna True se o serviço existir no banco de dados

#verifica se a reserva existe
def verifica_id_reserva_existe(cursor, id_reserva):
    cursor.execute('SELECT ID_reserva FROM RESERVA WHERE ID_reserva = %s', (id_reserva,)) # Executa o comando SQL
    return cursor.fetchone() is not None # Retorna True se a reserva existir no banco de dados

# Função para imprimir os dados do quartos de forma individual
def imprime_quarto_individual(linha):
    print("Numero do quarto: ", linha[0]) # Imprime cada coluna em uma nova linha, [] indica a coluna
    print("Tipo de quarto: ", linha[1])
    print("Capacidade do quarto: ", linha[2])
    print("Valor do quarto: ", linha[3])
    print("\n")

# verifica se o cliente existe no banco de dados por cpf
def nome_cliente_existe(cursor, Nome_cliente):
    cursor.execute('SELECT Nome_cliente FROM cliente WHERE Nome_cliente = %s', (Nome_cliente,))
    return cursor.fetchone() is not None

# verificar se quarto existe no banco de dados por tipo
def verifica_tipo_quarto_existe(cursor, tipo):
    cursor.execute('SELECT Tipo_quarto FROM QUARTO WHERE Tipo_quarto = %s', (tipo,))
    return cursor.fetchone() is not None # Retorna True se o quarto existir no banco de dados

# verificar se quarto existe no banco de dados por capacidade
def verifica_capacidade_quarto_existe(cursor, capacidade):
    cursor.execute('SELECT Capacidade_quarto FROM quarto WHERE Capacidade_quarto = %s', (capacidade,))
    return cursor.fetchone() is not None

# verificar se a reserva existe no banco de dados por id
def reserva_existe(cursor, ID_reserva):
    cursor.execute('SELECT ID_reserva FROM RESERVA WHERE ID_reserva = %s', (ID_reserva,))
    return cursor.fetchone() is not None

def imprime_reserva_individual(linha):
    print("ID da reserva: ", linha[0]) # Imprime cada coluna em uma nova linha, [] indica a coluna
    print("Data de entrada: ", linha[1])
    print("Data de saída: ", linha[2])
    print("CPF do cliente: ", linha[3])
    print("Número do quarto: ", linha[4])
    print("Valor da quarto: ", linha[5])
    print("Valor do serviço: ", linha[6])
    print("\n")

def buscar_reserva_por_cpf(cursor, cpf_cliente):
    cursor.execute('SELECT * FROM RESERVA R, ALOCA A WHERE R.ID_reserva = A.ID_reserva AND R.CLIENTE = %s', (cpf_cliente,))
    return cursor.fetchall()

def buscar_reserva_por_data(cursor, data):
    cursor.execute('SELECT * FROM RESERVA WHERE Data_check_in_reserva <= %s AND Data_check_out_reserva >= %s', (data, data))
    return cursor.fetchall()