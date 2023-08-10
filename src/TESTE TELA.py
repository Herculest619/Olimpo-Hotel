import tkinter as tk
import mysql.connector
import utils
import tkcalendar

# Connect to database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'barcelona619',
    'database': 'hotel'
}

db = mysql.connector.connect(**db_config)  # Conecta ao banco de dados
cursor = db.cursor()  # Cria um cursor para executar comandos SQL

# Função para exibir sucesso em uma janela popup
def popup_sucesso(mensagem):
    popup = tk.Tk() # Cria uma janela popup
    popup.wm_title("Sucesso!") # Define o título da janela
    popup.geometry("300x100") # Define a resolução da janela
    popup.resizable(False, False) # Impede que a janela seja redimensionada
    popup_label = tk.Label(popup, text=mensagem) # Cria um rótulo
    popup_label.pack(side="top", pady=10) # Define o lado e o espaçamento do rótulo
    popup_button = tk.Button(popup, text="OK", command=lambda: popup.destroy()) # Cria um botão para fechar a janela
    popup_button.pack(side="bottom", pady=10) # Define o lado e o espaçamento do botão
    popup.mainloop() # Inicia o loop principal da janela popup

# Função para exibir erro em uma janela popup
def popup_error(mensagem):
    popup = tk.Tk() # Cria uma janela popup
    popup.wm_title("Erro!") # Define o título da janela
    popup.geometry("300x100") # Define a resolução da janela
    popup.resizable(False, False) # Impede que a janela seja redimensionada
    popup_label = tk.Label(popup, text="Erro: " + mensagem) # Cria um rótulo
    popup_label.pack(side="top", pady=10) # Define o lado e o espaçamento do rótulo
    popup_button = tk.Button(popup, text="OK", command=lambda: popup.destroy()) # Cria um botão para fechar a janela
    popup_button.pack(side="bottom", pady=10) # Define o lado e o espaçamento do botão
    popup.mainloop() # Inicia o loop principal da janela popup

# Função para limpar o texto padrão da caixa de entrada
def clear_text(event):
    entry = event.widget
    if entry.get() == entry.default_text:
        entry.delete(0, "end")
        entry.config(foreground="black")

def imprimir_cliente_tabela(content_frame, cliente):

    def sort_column(col):
        items = table.get_children('')
        items = [(table.set(item, col), item) for item in items]
        items.sort()
        for index, (value, item) in enumerate(items):
            table.move(item, '', index)

        table.heading(col, command=lambda: sort_column(col))

    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(pady=10)

    table = tk.ttk.Treeview(table_frame, columns=(" ", "CPF", "Nome", "Telefone", "Endereço", "Data de nascimento", "CPF do titular"),
                                show="headings", height="15")
    table.pack(side="left", fill="both", expand=True)

    table_scroll = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table_scroll.pack(side="right", fill="y")
    table.configure(yscrollcommand=table_scroll.set)

    table.heading(" ", text="")
    table.heading("CPF", text="CPF", command=lambda: sort_column("CPF"))
    table.heading("Nome", text="Nome", command=lambda: sort_column("Nome"))
    table.heading("Telefone", text="Telefone", command=lambda: sort_column("Telefone"))
    table.heading("Endereço", text="Endereço", command=lambda: sort_column("Endereço"))
    table.heading("Data de nascimento", text="Data de nascimento", command=lambda: sort_column("Data de nascimento"))
    table.heading("CPF do titular", text="CPF do titular", command=lambda: sort_column("CPF do titular"))
    
    # Ajustar a largura das colunas manualmente (em pixels)
    table.column(" ", width=10)
    table.column("CPF", width=100)
    table.column("Nome", width=200)
    table.column("Telefone", width=100)
    table.column("Endereço", width=150)
    table.column("Data de nascimento", width=150)
    table.column("CPF do titular", width=100)

    i = 1
    for c in cliente:

        cpf = c[0] if c[0] is not None else ""
        nome = c[1] if c[1] is not None else ""
        telefone = c[2] if c[2] is not None else ""
        endereco = c[3] if c[3] is not None else ""
        data_nascimento = c[4] if c[4] is not None else ""
        cpf_titular = c[5] if c[5] is not None else ""
        
        table.insert("", "end", values=(i, cpf, nome, telefone, endereco, data_nascimento, cpf_titular))
        i += 1

def imprimir_cliente_acompanhante_tabela(content_frame, cliente):
    def sort_column(col):
        items = table.get_children('')
        items = [(table.set(item, col), item) for item in items]
        items.sort()
        for index, (value, item) in enumerate(items):
            table.move(item, '', index)

        table.heading(col, command=lambda: sort_column(col))

    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(pady=10)

    table = tk.ttk.Treeview(table_frame, columns=(" ", "CPF Titular", "Nome Titular", "CPF Acompanhante", "Nome Acompanhante"),
                                show="headings", height="15")
    table.pack(side="left", fill="both", expand=True)

    table_scroll = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table_scroll.pack(side="right", fill="y")
    table.configure(yscrollcommand=table_scroll.set)

    table.heading(" ", text="")
    table.heading("CPF Titular", text="CPF Titular", command=lambda: sort_column("CPF Titular"))
    table.heading("Nome Titular", text="Nome Titular", command=lambda: sort_column("Nome Titular"))
    table.heading("CPF Acompanhante", text="CPF Acompanhante", command=lambda: sort_column("CPF Acompanhante"))
    table.heading("Nome Acompanhante", text="Nome Acompanhante", command=lambda: sort_column("Nome Acompanhante"))

    # Ajustar a largura das colunas manualmente (em pixels)
    table.column(" ", width=10)
    table.column("CPF Titular", width=100)
    table.column("Nome Titular", width=200)
    table.column("CPF Acompanhante", width=100)
    table.column("Nome Acompanhante", width=200)

    i = 1
    for c in cliente:
        CPF_titular = c[0] if c[0] is not None else ""
        Nome_Titular = c[1] if c[1] is not None else ""
        CPF_Acompanhante = c[2] if c[2] is not None else ""
        Nome_Acompanhante = c[3] if c[3] is not None else ""

        table.insert("", "end", values=(i, CPF_titular, Nome_Titular, CPF_Acompanhante, Nome_Acompanhante))
        i += 1

# Função para imprimir os dados de um cliente em caixas de diálogo editáveis e um botão para excluir
def imprimir_cliente_editar_excluir(content_frame, cliente):
    def salvar_alteracoes():
        # Adicione aqui a lógica para salvar as alterações feitas nos campos de edição
        # e atualizar os dados do cliente no banco de dados.

        # Exiba uma mensagem de confirmação após salvar as alterações
        popup_sucesso("As alterações foram salvas com sucesso!")

    def excluir_cliente():
        # Adicione aqui a lógica para excluir o cliente do banco de dados.

        # Exiba uma mensagem de confirmação após excluir o cliente
        popup_sucesso("O cliente foi excluído com sucesso!")

    # Cria um novo frame para os campos de edição e exclusão
    edit_frame = tk.Frame(content_frame, bg="white")
    edit_frame.pack(pady=10)

    # Preencha os campos de edição com os valores do cliente, mantendo as caixas vazias para valores nulos
    cpf_label = tk.Label(edit_frame, text="CPF:")
    cpf_entry = tk.Entry(edit_frame, width=50)
    cpf_entry.insert(0, cliente[0] if cliente[0] is not None else "")
    cpf_label.pack(pady=5) # Espaçamento entre o rótulo e a caixa de entrada
    cpf_entry.pack(pady=5) # Espaçamento entre as caixas de entrada

    nome_label = tk.Label(edit_frame, text="Nome completo:")
    nome_entry = tk.Entry(edit_frame, width=50)
    nome_entry.insert(0, cliente[1] if cliente[1] is not None else "")
    nome_label.pack(pady=5)
    nome_entry.pack(pady=5)

    telefone_label = tk.Label(edit_frame, text="Telefone:")
    telefone_entry = tk.Entry(edit_frame, width=50)
    telefone_entry.insert(0, cliente[2] if cliente[2] is not None else "")
    telefone_label.pack(pady=5)
    telefone_entry.pack(pady=5)

    endereco_label = tk.Label(edit_frame, text="Endereço completo:")
    endereco_entry = tk.Entry(edit_frame, width=50)
    endereco_entry.insert(0, cliente[3] if cliente[3] is not None else "")
    endereco_label.pack(pady=5)
    endereco_entry.pack(pady=5)

    data_nascimento_label = tk.Label(edit_frame, text="Data de nascimento:")
    data_nascimento_entry = tk.Entry(edit_frame, width=50)
    data_nascimento_entry.insert(0, cliente[4] if cliente[4] is not None else "")
    data_nascimento_label.pack(pady=5)
    data_nascimento_entry.pack(pady=5)

    cpf_titular_label = tk.Label(edit_frame, text="CPF do titular:")
    cpf_titular_entry = tk.Entry(edit_frame, width=50)
    cpf_titular_entry.insert(0, cliente[5] if cliente[5] is not None else "")
    cpf_titular_label.pack(pady=5)
    cpf_titular_entry.pack(pady=5)


    # Adicione um botão para salvar as alterações, cor verde
    '''salvar_button = tk.Button(edit_frame, text="Salvar Alterações", command=salvar_alteracoes)
    salvar_button.pack(side="left", padx=25, pady=40)'''
    salvar_button = tk.Button(edit_frame, text="Salvar Alterações", command=salvar_alteracoes)
    salvar_button.configure(bg="green", fg="white")
    salvar_button.pack(side="left", padx=25, pady=40)



    # Adicione um botão para excluir o cliente
    excluir_button = tk.Button(edit_frame, text="Excluir Cliente", command=excluir_cliente)
    excluir_button.configure(bg="red", fg="white")
    excluir_button.pack(side="right", padx=25, pady=40)

# tela inicial
def main_menu(tela=None, menu_frame=None, content_frame=None):
    #remove o menu da tela se não for a primeira vez que a função é chamada
    if menu_frame is not None:
        menu_frame.pack_forget()
    # Remove the content frame if it exists
    if content_frame is not None:
        content_frame.pack_forget()

    # Cria a janela principal se for a primeira vez que a função é chamada
    if tela is None:
        tela = tk.Tk() # Cria a janela principal, tela é o nome da janela
        tela.title("Olimpo Hotel Management System") # Define o título da janela
        tela.geometry("1080x720") # Define a resolução da janela
        tela.resizable(False, False) # Impede que a janela seja redimensionada

    # Create the menu frame on the left
    menu_frame = tk.Frame(tela, bg="gray", width=300)   # Cria um frame para o menu
    menu_frame.pack(side="left", fill="y") # Define o lado e o preenchimento do frame, y=vertical

    # Create the content frame on the right
    content_frame = tk.Frame(tela, bg="white", width=780) # Cria um frame para o conteúdo
    content_frame.pack(side="right", fill="both", expand=True) # Define o lado e o preenchimento do frame, side=right, both=horizontal e vertical, expand=True para expandir o frame

    # Add a label to the menu frame
    menu_lateral_label = tk.Label(menu_frame, text="   MENU   ", font=("Arial", 18))
    menu_lateral_label.pack(side="top", pady=10)

    # Create the menu buttons
    clientes_button = tk.Button(menu_frame, text="Clientes") # Cria um botão para o menu
    reservas_button = tk.Button(menu_frame, text="Reservas") # Cria um botão para o menu
    quartos_button = tk.Button(menu_frame, text="Quartos")  # Cria um botão para o menu
    servicos_button = tk.Button(menu_frame, text="Serviços") # Cria um botão para o menu
    sair_button = tk.Button(menu_frame, text="Sair", command=tela.quit) # Cria um botão para o menu

    # Add the menu buttons to the menu frame
    clientes_button.pack(side="top", pady=10, padx=10) # Define o lado e o espaçamento do botão
    reservas_button.pack(side="top", pady=10, padx=10) #side=lado, pady=espaçamento em y, padx=espaçamento em x
    quartos_button.pack(side="top", pady=10, padx=10)
    servicos_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão
 
    #adiciona função ao botão clientes
    clientes_button.config(command=lambda: cliente_menu(tela, menu_frame, content_frame)) # Define a função do botão

    # Add a label to the content frame
    content_label = tk.Label(content_frame, text="Olimpo Hotel Management System!", font=("Helvetica", 24))
    content_label.pack(pady=50) # Define o espaçamento do label


    # Start the main loop
    tela.mainloop() # Inicia o loop principal

# tela de clientes
def cliente_menu(tela, menu_frame, content_frame):
    # Remove the menu frame
    menu_frame.pack_forget() 
    #remove o conteúdo da tela
    content_frame.pack_forget()

    # Create the menu frame on the left
    menu_frame = tk.Frame(tela, bg="gray", width=300)   # Cria um frame para o menu
    menu_frame.pack(side="left", fill="y") # Define o lado e o preenchimento do frame, y=vertical

    # cria o frame do conteúdo, frame = quadro
    content_frame = tk.Frame(tela, bg="white", width=780)
    content_frame.pack(side="right", fill="both", expand=True)

    # Adiciona um label ao menu_frame
    clientes_label = tk.Label(menu_frame, text="CLIENTES", font=("Arial", 18))
    clientes_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_client_button = tk.Button(menu_frame, text="Cadastrar") # Cria um botão para o menu
    buscar_client_button = tk.Button(menu_frame, text="Buscar") # Cria um botão para o menu
    listar_client_button = tk.Button(menu_frame, text="Listar")  # Cria um botão para o menu
    voltar_client_button = tk.Button(menu_frame, text="Voltar", command=lambda: main_menu(tela, menu_frame, content_frame)) # Cria um botão para o menu
    sair_button = tk.Button(menu_frame, text="Sair", command=tela.quit) # Cria um botão para o menu

    # adiciona os botões ao menu
    cadastrar_client_button.pack(side="top", pady=10, padx=10) # Define o lado e o espaçamento do botão
    buscar_client_button.pack(side="top", pady=10, padx=10) #side=lado, pady=espaçamento em y, padx=espaçamento em x
    listar_client_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão
    voltar_client_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão
    
    #adiciona função dos botões
    cadastrar_client_button.config(command=lambda: cadastrar_cliente_menu(tela, menu_frame, content_frame)) # Define a função do botão
    buscar_client_button.config(command=lambda: buscar_cliente_menu(tela, menu_frame, content_frame)) # Define a função do botão
    listar_client_button.config(command=lambda: listar_clientes_menu(tela, menu_frame, content_frame)) # Define a função do botão

    # Add a label to the content frame
    content_label = tk.Label(content_frame, text="Olimpo Hotel Management System!", font=("Helvetica", 24))
    content_label.pack(pady=50) # Define o espaçamento do label

#tela de cadastrar clientes
def cadastrar_cliente_menu(tela, menu_frame, content_frame):
    # Remove the menu frame
    menu_frame.pack_forget() 
    #remove o conteúdo da tela
    content_frame.pack_forget()

    # Create the menu frame on the left
    menu_frame = tk.Frame(tela, bg="gray", width=300)   # Cria um frame para o menu
    menu_frame.pack(side="left", fill="y") # Define o lado e o preenchimento do frame, y=vertical

    # cria o frame do conteúdo, frame = quadro
    content_frame = tk.Frame(tela, bg="white", width=780)
    content_frame.pack(side="right", fill="both", expand=True)

    # Adiciona um label ao menu_frame
    clientes_label = tk.Label(menu_frame, text="CADASTRAR\nCLIENTE", font=("Arial", 18))
    clientes_label.pack(side="top", pady=10)


    # cria os botões do menu
    cadastrar_client_button = tk.Button(menu_frame, text="Cadastrar") # Cria um botão para o menu
    cadastrar_client_button.configure(bg="black", fg="white") # Altera a cor do botão
    buscar_client_button = tk.Button(menu_frame, text="Buscar") # Cria um botão para o menu
    listar_client_button = tk.Button(menu_frame, text="Listar")  # Cria um botão para o menu
    voltar_client_button = tk.Button(menu_frame, text="Voltar", command=lambda: main_menu(tela, menu_frame, content_frame)) # Cria um botão para o menu
    sair_button = tk.Button(menu_frame, text="Sair", command=tela.quit) # Cria um botão para o menu

    # adiciona os botões ao menu
    cadastrar_client_button.pack(side="top", pady=10, padx=10) # Define o lado e o espaçamento do botão
    buscar_client_button.pack(side="top", pady=10, padx=10) #side=lado, pady=espaçamento em y, padx=espaçamento em x
    listar_client_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão
    voltar_client_button.pack(side="bottom", pady=10, fill="x") # Define o lado

    #adiciona função dos botões
    buscar_client_button.config(command=lambda: buscar_cliente_menu(tela, menu_frame, content_frame)) # Define a função do botão
    listar_client_button.config(command=lambda: listar_clientes_menu(tela, menu_frame, content_frame)) # Define a função do botão

    # cria as caixas de diálogo
    nome_label = tk.Label(content_frame, text="Nome completo:")
    nome_entry = tk.Entry(content_frame, width=50)
    nome_entry.default_text = "João da Silva"  # Texto padrão
    nome_entry.insert(0, nome_entry.default_text)
    nome_entry.config(foreground="gray")
    nome_label.pack(pady=5)  # Espaçamento entre o rótulo e a caixa de entrada
    nome_entry.pack(pady=5)  # Espaçamento entre as caixas de entrada
    nome_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco


    cpf_label = tk.Label(content_frame, text="CPF:")
    cpf_entry = tk.Entry(content_frame, width=50)
    cpf_entry.default_text = "12345678900"  # Texto padrão
    cpf_entry.insert(0, cpf_entry.default_text)
    cpf_entry.config(foreground="gray")
    cpf_label.pack(pady=5)
    cpf_entry.pack(pady=5)
    cpf_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    telefone_label = tk.Label(content_frame, text="Telefone:")
    telefone_entry = tk.Entry(content_frame, width=50)
    telefone_entry.default_text = "31 91234-5678"  # Texto padrão
    telefone_entry.insert(0, telefone_entry.default_text)
    telefone_entry.config(foreground="gray")
    telefone_label.pack(pady=5)
    telefone_entry.pack(pady=5)
    telefone_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    endereco_label = tk.Label(content_frame, text="Endereço completo:")
    endereco_entry = tk.Entry(content_frame, width=50)
    endereco_entry.default_text = "Rua Exemplo, 123"  # Texto padrão
    endereco_entry.insert(0, endereco_entry.default_text)
    endereco_entry.config(foreground="gray")
    endereco_label.pack(pady=5)
    endereco_entry.pack(pady=5)
    endereco_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    nascimento_label = tk.Label(content_frame, text="Data de nascimento:")
    nascimento_entry = tkcalendar.DateEntry(content_frame, width=12, date_pattern='yyyy/mm/dd', background="gray", foreground="black")
    nascimento_entry.set_date('2000-01-01')  # Define a data padrão
    nascimento_label.pack(pady=5)
    nascimento_entry.pack(pady=5)

    cpf_titular_label = tk.Label(content_frame, text="CPF do titular:")
    cpf_titular_entry = tk.Entry(content_frame, width=50)
    cpf_titular_entry.default_text = "12345678900"  # Texto padrão
    cpf_titular_entry.insert(0, cpf_titular_entry.default_text)
    cpf_titular_entry.config(foreground="gray")
    cpf_titular_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    # Função para mostrar a caixa de entrada do CPF do titular
    def toggle_acompanhante():
        if acompanhante_var.get() == 1:
            cpf_titular_label.pack(pady=5) # Espaçamento entre o rótulo e a caixa de entrada
            cpf_titular_entry.pack(pady=10) # Espaçamento entre as caixas de entrada
        else:
            cpf_titular_label.pack_forget()
            cpf_titular_entry.pack_forget()

    acompanhante_var = tk.IntVar()
    acompanhante_checkbutton = tk.Checkbutton(content_frame, text="Acompanhante?", variable=acompanhante_var, command=toggle_acompanhante)
    acompanhante_checkbutton.pack(pady=10)

    # Função para salvar os dados no banco de dados
    def save_to_database_client():

        try:
            Nome_cliente = nome_entry.get()
            # Verifique se o nome do cliente está vazio
            if not Nome_cliente:
                nome_entry.config(foreground="red")  # Altera a cor do rótulo para vermelho
                cpf_entry.delete(0, "end") #limpar caixa de entrada
                nome_entry.insert(0, "NÃO PODE SER NULL") # Exibe uma mensagem de erro
                return # Retorna para a função anterior
            
            CPF = cpf_entry.get()
            if not utils.validar_cpf(CPF):  # Se o CPF não for válido
                cpf_entry.config(foreground="red")  # Altera a cor do rótulo para vermelho
                cpf_entry.delete(0, "end") #limpar caixa de entrada
                cpf_entry.insert(0, "CPF INVÁLIDO") # Exibe uma mensagem de erro
                return # Retorna para a função anterior
            if utils.cpf_existe(cursor, CPF): # Se o CPF já existir no banco de dados
                cpf_entry.config(foreground="red")  # Altera a cor do rótulo para vermelho
                cpf_entry.delete(0, "end") #limpar caixa de entrada
                cpf_entry.insert(0, "CPF JÁ EXISTE") # Exibe uma mensagem de erro
                return # Retorna para a função anterior
            cursor.fetchall() #limpa o cursor
            
            Telefone_cliente = telefone_entry.get()

            Endereco_cliente = endereco_entry.get()

            Data_nasc_cliente = nascimento_entry.get()

            CPF_TITULAR = cpf_titular_entry.get() if acompanhante_var.get() == 1 else None # Se o acompanhante for marcado, pegue o CPF do titular
            if CPF_TITULAR == "":  # Se o CPF do titular for vazio
                CPF_TITULAR = None  # Defina como None
            if CPF_TITULAR and not utils.cpf_existe(cursor, CPF_TITULAR): # Se o CPF do titular não existir no banco de dados
                cpf_titular_entry.config(foreground="red")  # Altera a cor do rótulo para vermelho
                cpf_titular_entry.delete(0, "end") #limpar caixa de entrada
                cpf_titular_entry.insert(0, "CPF NÃO EXISTE") # Exibe uma mensagem de erro
                return # Retorna para a função anterior
            cursor.fetchall() #limpa o cursor

            # Insere os dados na tabela
            cursor.execute('INSERT INTO cliente (CPF, Nome_cliente, Telefone_cliente, Endereco_cliente, Data_nasc_cliente, CPF_TITULAR) VALUES (%s, %s, %s, %s, %s, %s)',
                        (CPF, Nome_cliente, Telefone_cliente, Endereco_cliente, Data_nasc_cliente, CPF_TITULAR))  # Executa o comando SQL
            db.commit()  # Salva as alterações no banco de dados

            # Exibe uma mensagem de sucesso com um popup e retorna para o menu de clientes
            popup_sucesso("Cliente cadastrado com sucesso!") # Exibe uma mensagem de sucesso
            cliente_menu(tela, menu_frame, content_frame) # Retorna para o menu de clientes

        except Exception as e:
            popup_error(str(e)) # Exibe uma mensagem de erro
            main_menu(tela, menu_frame, content_frame) # Retorna para o menu principal


    salvar_button = tk.Button(content_frame, text="SALVAR", command=save_to_database_client)
    salvar_button.configure(bg="blue", fg="white")
    salvar_button.pack(pady=50)

#tela de buscar cliente
def buscar_cliente_menu(tela, menu_frame, content_frame):
    # Remove the menu frame
    menu_frame.pack_forget() 
    #remove o conteúdo da tela
    content_frame.pack_forget()

    # Create the menu frame on the left
    menu_frame = tk.Frame(tela, bg="gray", width=300)   # Cria um frame para o menu
    menu_frame.pack(side="left", fill="y") # Define o lado e o preenchimento do frame, y=vertical

    # cria o frame do conteúdo, frame = quadro
    content_frame = tk.Frame(tela, bg="white", width=780)
    content_frame.pack(side="right", fill="both", expand=True)

    # Adiciona um label ao menu_frame
    clientes_label = tk.Label(menu_frame, text="BUSCAR\nCLIENTE", font=("Arial", 18))
    clientes_label.pack(side="top", pady=10)


    # cria os botões do menu
    cadastrar_client_button = tk.Button(menu_frame, text="Cadastrar") # Cria um botão para o menu
    buscar_client_button = tk.Button(menu_frame, text="Buscar") # Cria um botão para o menu
    buscar_client_button.configure(bg="black", fg="white") # Altera a cor do botão
    listar_client_button = tk.Button(menu_frame, text="Listar")  # Cria um botão para o menu
    voltar_client_button = tk.Button(menu_frame, text="Voltar", command=lambda: main_menu(tela, menu_frame, content_frame)) # Cria um botão para o menu
    sair_button = tk.Button(menu_frame, text="Sair", command=tela.quit) # Cria um botão para o menu

    # adiciona os botões ao menu
    cadastrar_client_button.pack(side="top", pady=10, padx=10) # Define o lado e o espaçamento do botão
    buscar_client_button.pack(side="top", pady=10, padx=10) #side=lado, pady=espaçamento em y, padx=espaçamento em x
    listar_client_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão
    voltar_client_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão

    #adiciona função dos botões
    cadastrar_client_button.config(command=lambda: cadastrar_cliente_menu(tela, menu_frame, content_frame)) # Define a função do botão
    listar_client_button.config(command=lambda: listar_clientes_menu(tela, menu_frame, content_frame)) # Define a função do botão

    # cria uma caixa de seleção com as opções de busca, CPF e nome ao lado da caixa de entrada, e abaixo um botão para buscar
    buscar_label = tk.Label(content_frame, text="Buscar por:")
    buscar_label.pack(pady=5)
    buscar_var = tk.StringVar()
    buscar_combobox = tk.ttk.Combobox(content_frame, width=12, textvariable=buscar_var, state="readonly")
    buscar_combobox["values"] = ["CPF", "Nome"]
    buscar_combobox.current(0)  # Define o valor padrão
    buscar_combobox.pack(pady=5)

    buscar_entry = tk.Entry(content_frame, width=50)
    buscar_entry.default_text = "12345678900"  # Texto padrão
    buscar_entry.insert(0, buscar_entry.default_text)
    buscar_entry.config(foreground="gray")
    buscar_entry.pack(pady=5)
    buscar_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    # Função para buscar os dados no banco de dados
    def search_in_database_client():
        try:
            if buscar_var.get() == "CPF":
                CPF = buscar_entry.get()
                if not utils.validar_cpf(CPF):
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "CPF INVÁLIDO")
                    return
                
                if not utils.cpf_existe(cursor, CPF):
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "CPF NÃO ENCONTRADO")
                    return
                cursor.fetchall()

                cursor.execute('SELECT COUNT(*) FROM cliente WHERE CPF = %s', (CPF,))
                count = cursor.fetchone()[0]
                cursor.execute('SELECT * FROM cliente WHERE CPF = %s', (CPF,))  # Executa o comando SQL
                
                if count > 1:
                    cliente = cursor.fetchall()  # Pega os dados do cliente
                    imprimir_cliente_tabela(content_frame, cliente)
                else:
                    cliente = cursor.fetchone()  # Pega os dados do cliente
                    imprimir_cliente_editar_excluir(content_frame, cliente)
                
            elif buscar_var.get() == "Nome":
                Nome_cliente = buscar_entry.get()
                if not Nome_cliente:
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "NÃO PODE SER NULL")
                    return
                
                if not utils.nome_cliente_existe(cursor, Nome_cliente):
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "NOME NÃO ENCONTRADO")
                    return

                cursor.execute('SELECT COUNT(*) FROM cliente WHERE Nome_cliente = %s', (Nome_cliente,))
                count = cursor.fetchone()[0]
                cursor.execute('SELECT * FROM cliente WHERE Nome_cliente = %s', (Nome_cliente,))
                

                # Exibe os dados de varios clientes em uma tabela em um frame na tela de busca, cada cliente em uma linha, caso haja mais de um cliente com o mesmo nome
                if count > 1: #conta quantos clientes tem o mesmo nome
                    cliente = cursor.fetchall()
                    imprimir_cliente_tabela(content_frame, cliente)

                #exibe os dados de um cliente em caixas de dialogo em um frame na tela de busca
                else:
                    cliente = cursor.fetchone()
                    imprimir_cliente_editar_excluir(content_frame, cliente)

        # Caso ocorra algum erro
        except Exception as e:
            popup_error(str(e)) # Exibe uma mensagem de erro
            main_menu(tela, menu_frame, content_frame) # Retorna para o menu principal

    
    
    buscar_button = tk.Button(content_frame, text="BUSCAR", command=search_in_database_client)
    buscar_button.configure(bg="blue", fg="white")
    buscar_button.pack(pady=15)

#tela de listar clientes
def listar_clientes_menu(tela, menu_frame, content_frame):
    # Remove the menu frame
    menu_frame.pack_forget() 
    #remove o conteúdo da tela
    content_frame.pack_forget()

    # Create the menu frame on the left
    menu_frame = tk.Frame(tela, bg="gray", width=300)   # Cria um frame para o menu
    menu_frame.pack(side="left", fill="y") # Define o lado e o preenchimento do frame, y=vertical

    # cria o frame do conteúdo, frame = quadro
    content_frame = tk.Frame(tela, bg="white", width=780)
    content_frame.pack(side="right", fill="both", expand=True)

    # Adiciona um label ao menu_frame
    clientes_label = tk.Label(menu_frame, text="LISTAR\nCLIENTES", font=("Arial", 18)) 
    clientes_label.pack(side="top", pady=10)
    
    # cria os botões do menu
    cadastrar_client_button = tk.Button(menu_frame, text="Cadastrar") # Cria um botão para o menu
    buscar_client_button = tk.Button(menu_frame, text="Buscar") # Cria um botão para o menu
    listar_client_button = tk.Button(menu_frame, text="Listar")  # Cria um botão para o menu
    listar_client_button.configure(bg="black", fg="white") # Altera a cor do botão
    voltar_client_button = tk.Button(menu_frame, text="Voltar", command=lambda: main_menu(tela, menu_frame, content_frame)) # Cria um botão para o menu
    sair_button = tk.Button(menu_frame, text="Sair", command=tela.quit) # Cria um botão para o menu

    # adiciona os botões ao menu
    cadastrar_client_button.pack(side="top", pady=10, padx=10) # Define o lado e o espaçamento do botão
    buscar_client_button.pack(side="top", pady=10, padx=10) #side=lado, pady=espaçamento em y, padx=espaçamento em x
    listar_client_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão
    voltar_client_button.pack(side="bottom", pady=10, fill="x") # Define o lado

    #adiciona função dos botões
    cadastrar_client_button.config(command=lambda: cadastrar_cliente_menu(tela, menu_frame, content_frame)) # Define a função do botão
    buscar_client_button.config(command=lambda: buscar_cliente_menu(tela, menu_frame, content_frame)) # Define a função do botão

    #adicionar 3 botões no topo do content_frame para listar todos os clientes, listar clientes Titulares e listar clientes Acompanhantes
    listar_todos_button = tk.Button(content_frame, text="Listar todos", command=lambda: listar_todos_clientes(content_frame))
    listar_todos_button.pack(side="top", pady=10, padx=10, fill="x")
    
    listar_titulares_button = tk.Button(content_frame, text="Listar titulares", command=lambda: listar_titulares_clientes(content_frame))
    listar_titulares_button.pack(side="top", pady=10, padx=10, fill="x")

    listar_acompanhantes_button = tk.Button(content_frame, text="Listar acompanhantes", command=lambda: listar_acompanhantes_clientes(content_frame))
    listar_acompanhantes_button.pack(side="top", pady=10, padx=10, fill="x")

    listar_acomp_e_clien = tk.Button(content_frame, text="Listar acompanhantes e clientes", command=lambda: listar_acompanhantes_e_clientes(content_frame))
    listar_acomp_e_clien.pack(side="top", pady=10, padx=10, fill="x")

# Função para listar todos os clientes
def listar_todos_clientes(content_frame):
    try:
        cursor.execute('SELECT COUNT(*) FROM cliente')
        count = cursor.fetchone()[0]

        if count < 1: # Se não houver clientes
            popup_error("Não há clientes!") # Exibe uma mensagem de erro
        else:
            #cursor.fetchall() #limpa o cursor
            cursor.execute('SELECT * FROM cliente')  # Executa o comando SQL
            cliente = cursor.fetchall()  # Pega os dados do cliente
            imprimir_cliente_tabela(content_frame, cliente)

    except Exception as e:
        popup_error(str(e)) # Exibe uma mensagem de erro

# Função para listar todos os clientes titulares
def listar_titulares_clientes(content_frame):
    try:
        cursor.execute('SELECT COUNT(*) FROM cliente WHERE CPF_TITULAR IS NULL') # Executa o comando SQL
        count = cursor.fetchone()[0] # Pega o resultado da consulta
        
        if count < 1: # Se não houver clientes titulares
            popup_error("Não há clientes titulares!") # Exibe uma mensagem de erro
        else:
            cursor.execute('SELECT * FROM cliente WHERE CPF_TITULAR IS NULL')  # Executa o comando SQL
            cliente = cursor.fetchall()  # Pega os dados do cliente
            imprimir_cliente_tabela(content_frame, cliente) # Exibe os dados do cliente em uma tabela

    except Exception as e:
        popup_error(str(e)) # Exibe uma mensagem de erro

def listar_acompanhantes_clientes(content_frame):
    try:
        cursor.execute('SELECT COUNT(*) FROM cliente WHERE CPF_TITULAR IS NOT NULL') # Executa o comando SQL
        count = cursor.fetchone()[0] # Pega o resultado da consulta

        if count < 1: # Se não houver clientes acompanhantes
            popup_error("Não há clientes acompanhantes!") # Exibe uma mensagem de erro
        else:
            cursor.execute('SELECT * FROM cliente WHERE CPF_TITULAR IS NOT NULL')
            cliente = cursor.fetchall()  # Pega os dados do cliente
            imprimir_cliente_tabela(content_frame, cliente) # Exibe os dados do cliente em uma tabela

    except Exception as e:
        popup_error(str(e))

# Função para listar todos os clientes acompanhantes
def listar_acompanhantes_e_clientes(content_frame):
    try:
        cursor.execute('SELECT COUNT(*) FROM cliente WHERE CPF_TITULAR IS NOT NULL') # Executa o comando SQL
        count = cursor.fetchone()[0] # Pega o resultado da consulta

        if count < 1: # Se não houver clientes acompanhantes
            popup_error("Não há clientes acompanhantes!") # Exibe uma mensagem de erro
        else:

            consulta = """
                        SELECT T.CPF AS CPF_Titular,
                               T.Nome_cliente AS Nome_Titular,
                               A.CPF AS CPF_Acompanhante,
                               A.Nome_cliente AS Nome_Acompanhante
                        FROM 
                               CLIENTE T, CLIENTE A 
                        WHERE 
                               T.CPF = A.CPF_TITULAR;
                    """

            #cursor.execute('SELECT * FROM cliente T, cliente A WHERE A.CPF_TITULAR IS NOT NULL')
            cursor.execute(consulta)

            cliente = cursor.fetchall()  # Pega os dados do cliente
            imprimir_cliente_acompanhante_tabela(content_frame, cliente) # Exibe os dados do cliente em uma tabela
    except Exception as e:
        popup_error(str(e))

# Start the main menu
main_menu()