import tkinter as tk
import mysql.connector
import utils
import tkcalendar
import datetime

# Connect to database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'hotel'
}

db = mysql.connector.connect(**db_config)  # Conecta ao banco de dados
cursor = db.cursor()  # Cria um cursor para executar comandos SQL

# Função para exibir sucesso em uma janela popup
def popup_sucesso(mensagem):
    popup = tk.Tk() # Cria uma janela popup
    popup.wm_title("Sucesso!") # Define o título da janela

    # Ajusta o tamanho da janela de acordo com o tamanho do texto
    width = max(300, len(mensagem) * 8)
    height = 100

    popup.geometry(f"{width}x{height}") # Define a resolução da janela
    popup.resizable(False, False) # Impede que a janela seja redimensionada

    popup_label = tk.Label(popup, text=mensagem, wraplength=width-20) # Cria um rótulo com ajuste de texto
    popup_label.pack(side="top", pady=10) # Define o lado e o espaçamento do rótulo

    popup_button = tk.Button(popup, text="OK", command=lambda: popup.destroy()) # Cria um botão para fechar a janela
    popup_button.pack(side="bottom", pady=10) # Define o lado e o espaçamento do botão

    popup.mainloop() # Inicia o loop principal da janela popup

# Função para exibir erro em uma janela popup
def popup_error(mensagem):
    popup = tk.Tk() # Cria uma janela popup
    popup.wm_title("Erro!") # Define o título da janela

    # Ajusta o tamanho da janela de acordo com o tamanho do texto
    width = max(300, len(mensagem) * 8)
    height = 100

    popup.geometry(f"{width}x{height}") # Define a resolução da janela
    popup.resizable(False, False) # Impede que a janela seja redimensionada

    popup_label = tk.Label(popup, text="Erro: " + mensagem, wraplength=width-20) # Cria um rótulo com ajuste de texto
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
    quartos_button.config(command=lambda: quarto_menu(tela, menu_frame, content_frame)) # Define a função do botão
    reservas_button.config(command=lambda: reserva_menu(tela, menu_frame, content_frame)) # Define a função do botão
    servicos_button.config(command=lambda: servico_menu(tela, menu_frame, content_frame)) # Define a função do botão

    # Add a label to the content frame
    content_label = tk.Label(content_frame, text="Olimpo Hotel Management System!", font=("Helvetica", 24))
    content_label.pack(pady=50) # Define o espaçamento do label


    # Start the main loop
    tela.mainloop() # Inicia o loop principal



# CLIENTE
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
    table.column(" ", width=10, anchor="center")
    table.column("CPF", width=100, anchor="center")
    table.column("Nome", width=200, anchor="center")
    table.column("Telefone", width=100, anchor="center")
    table.column("Endereço", width=150, anchor="center")
    table.column("Data de nascimento", width=150, anchor="center")
    table.column("CPF do titular", width=100, anchor="center")

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
    table.column(" ", width=10, anchor="center")
    table.column("CPF Titular", width=100, anchor="center")
    table.column("Nome Titular", width=200, anchor="center")
    table.column("CPF Acompanhante", width=100, anchor="center")
    table.column("Nome Acompanhante", width=200, anchor="center")

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
    # Limpar todos os widgets existentes no content_frame
    # for widget in content_frame.winfo_children():
    #    widget.destroy()
        
    def salvar_alteracoes():
        try:
            # Atualize os valores do cliente com base nos campos de edição
            novo_cpf = cpf_entry.get()
            if not utils.validar_cpf(novo_cpf):  # Se o CPF não for válido
                cpf_entry.config(foreground="red")  # Altera a cor do rótulo para vermelho
                cpf_entry.delete(0, "end") #limpar caixa de entrada
                cpf_entry.insert(0, "CPF INVÁLIDO") # Exibe uma mensagem de erro
                return # Retorna para a função anterior
            '''if utils.cpf_existe(cursor, novo_cpf): # Se o CPF já existir no banco de dados
                cpf_entry.config(foreground="red")  # Altera a cor do rótulo para vermelho
                cpf_entry.delete(0, "end") #limpar caixa de entrada
                cpf_entry.insert(0, "CPF JÁ EXISTE") # Exibe uma mensagem de erro
                return # Retorna para a função anterior
            cursor.fetchall() #limpa o cursor'''

            novo_nome = nome_entry.get()
            if not novo_nome:
                nome_entry.config(foreground="red")  # Altera a cor do rótulo para vermelho
                cpf_entry.delete(0, "end") #limpar caixa de entrada
                nome_entry.insert(0, "NÃO PODE SER NULL") # Exibe uma mensagem de erro
                return # Retorna para a função anterior
            
            novo_telefone = telefone_entry.get()
            novo_endereco = endereco_entry.get()

            nova_data_nascimento = data_nascimento_entry.get_date()  # Obtém a data do DateEntry
            if not nova_data_nascimento:
                data_nascimento_entry.config(foreground="red")
                cpf_entry.delete(0, "end") #limpar caixa de entrada
                data_nascimento_entry.insert(0, "NÃO PODE SER NULL")
                return
            
            novo_cpf_titular = cpf_titular_entry.get()
            if novo_cpf_titular == "":  # Se o CPF do titular for vazio
                novo_cpf_titular = None  # Defina como None
            if novo_cpf_titular and not utils.cpf_existe(cursor, novo_cpf_titular): # Se o CPF do titular não existir no banco de dados
                cpf_titular_entry.config(foreground="red")  # Altera a cor do rótulo para vermelho
                cpf_titular_entry.delete(0, "end") #limpar caixa de entrada
                cpf_titular_entry.insert(0, "CPF NÃO EXISTE") # Exibe uma mensagem de erro
                return # Retorna para a função anterior
            cursor.fetchall() #limpa o cursor

            # Atualize os valores do cliente com base nos campos de edição
            cursor.execute('UPDATE cliente SET CPF = %s, Nome_cliente = %s, Telefone_cliente = %s, Endereco_cliente = %s, Data_nasc_cliente = %s, CPF_TITULAR = %s WHERE CPF = %s',
                        (novo_cpf, novo_nome, novo_telefone, novo_endereco, nova_data_nascimento, novo_cpf_titular, cliente[0]))
            
            db.commit() # Salva as alterações no banco de dados

            # Exiba uma mensagem de confirmação após salvar as alterações
            popup_sucesso("As alterações foram salvas com sucesso!")

        except mysql.connector.Error as err:
            popup_error(str(err))

    def excluir_cliente():
        try:
            # Exclua o cliente com base no CPF
            cursor.execute('DELETE FROM cliente WHERE CPF = %s', (cliente[0],))
            db.commit() # Salva as alterações no banco de dados

            # Exiba uma mensagem de confirmação após excluir o cliente
            popup_sucesso("O cliente foi excluído com sucesso!")

        except mysql.connector.Error as err:
            popup_error(str(err))

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
    data_nascimento_entry = tkcalendar.DateEntry(edit_frame, width=12, date_pattern='yyyy/mm/dd', background="gray", foreground="black")
    data_nascimento_entry.set_date(cliente[4] if cliente[4] is not None else "")
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
            if not Data_nasc_cliente:
                nascimento_entry.config(foreground="red")
                cpf_entry.delete(0, "end") #limpar caixa de entrada
                nascimento_entry.insert(0, "NÃO PODE SER NULL")
                return

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



# QUARTO
def quarto_menu(tela, menu_frame, content_frame):
    # Remove the menu frame
    menu_frame.pack_forget() 
    #remove o conteúdo da tela
    content_frame.pack_forget()

    # Create the menu frame on the left
    menu_quarto_frame = tk.Frame(tela, bg="gray", width=300)   # Cria um frame para o menu
    menu_quarto_frame.pack(side="left", fill="y") # Define o lado e o preenchimento do frame, y=vertical

    # cria o frame do conteúdo, frame = quadro
    content_quarto_frame = tk.Frame(tela, bg="white", width=780)
    content_quarto_frame.pack(side="right", fill="both", expand=True)

    # Adiciona um label ao menu_frame
    quarto_label = tk.Label(menu_quarto_frame, text="QUARTOS", font=("Arial", 18))
    quarto_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_quarto_button = tk.Button(menu_quarto_frame, text="Cadastrar") # Cria um botão para o menu
    buscar_quarto_button = tk.Button(menu_quarto_frame, text="Buscar") # Cria um botão para o menu
    listar_quarto_button = tk.Button(menu_quarto_frame, text="Listar")  # Cria um botão para o menu
    voltar_quarto_button = tk.Button(menu_quarto_frame, text="Voltar", command=lambda: main_menu(tela, menu_quarto_frame, content_quarto_frame)) # Cria um botão para o menu
    sair_button = tk.Button(menu_quarto_frame, text="Sair", command=tela.quit) # Cria um botão para o menu

    # adiciona os botões ao menu
    cadastrar_quarto_button.pack(side="top", pady=10, padx=10) # Define o lado e o espaçamento do botão
    buscar_quarto_button.pack(side="top", pady=10, padx=10) #side=lado, pady=espaçamento em y, padx=espaçamento em x
    listar_quarto_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão
    voltar_quarto_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão

    #adiciona função dos botões
    cadastrar_quarto_button.config(command=lambda: cadastrar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame)) # Define a função do botão
    buscar_quarto_button.config(command=lambda: buscar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame)) # Define a função do botão
    listar_quarto_button.config(command=lambda: listar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame)) # Define a função do botão

    # adicionar label ao content_frame
    content_label = tk.Label(content_quarto_frame, text="Olimpo Hotel Management System!", font=("Helvetica", 24))
    content_label.pack(pady=50) # Define o espaçamento do label

#tela de cadastrar quarto
def cadastrar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame):
    # remove o menu frame
    menu_quarto_frame.pack_forget()
    # remove o conteúdo da tela
    content_quarto_frame.pack_forget()

    # cria o menu frame
    menu_quarto_frame = tk.Frame(tela, bg="gray", width=300)
    menu_quarto_frame.pack(side="left", fill="y")

    # cria o frame do conteúdo
    content_quarto_frame = tk.Frame(tela, bg="white", width=780)
    content_quarto_frame.pack(side="right", fill="both", expand=True)

    # adiciona um label ao menu_frame
    quarto_label = tk.Label(menu_quarto_frame, text="CADASTRAR\nQUARTO", font=("Arial", 18))
    quarto_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_quarto_button = tk.Button(menu_quarto_frame, text="Cadastrar")
    cadastrar_quarto_button.configure(bg="black", fg="white")
    buscar_quarto_button = tk.Button(menu_quarto_frame, text="Buscar")
    listar_quarto_button = tk.Button(menu_quarto_frame, text="Listar")
    voltar_quarto_button = tk.Button(menu_quarto_frame, text="Voltar", command=lambda: main_menu(tela, menu_quarto_frame, content_quarto_frame))
    sair_button = tk.Button(menu_quarto_frame, text="Sair", command=tela.quit)

    # adiciona os botões ao menu
    cadastrar_quarto_button.pack(side="top", pady=10, padx=10)
    buscar_quarto_button.pack(side="top", pady=10, padx=10)
    listar_quarto_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_quarto_button.pack(side="bottom", pady=10, fill="x")

    # adiciona função dos botões
    buscar_quarto_button.config(command=lambda: buscar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame))
    listar_quarto_button.config(command=lambda: listar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame))

    # cria as caixas de diálogo
    numero_label = tk.Label(content_quarto_frame, text="Número do quarto:")
    numero_entry = tk.Entry(content_quarto_frame, width=50)
    numero_entry.default_text = "123"  # Texto padrão
    numero_entry.insert(0, numero_entry.default_text)
    numero_entry.config(foreground="gray")
    numero_label.pack(pady=5)  # Espaçamento entre o rótulo e a caixa de entrada
    numero_entry.pack(pady=5)  # Espaçamento entre as caixas de entrada
    numero_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    tipo_label = tk.Label(content_quarto_frame, text="Tipo do quarto:")
    tipo_entry = tk.Entry(content_quarto_frame, width=50)
    tipo_entry.default_text = "Simples"  # Texto padrão
    tipo_entry.insert(0, tipo_entry.default_text)
    tipo_entry.config(foreground="gray")
    tipo_label.pack(pady=5)
    tipo_entry.pack(pady=5)
    tipo_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    capacidade_label = tk.Label(content_quarto_frame, text="Capacidade do quarto:")
    capacidade_entry = tk.Entry(content_quarto_frame, width=50)
    capacidade_entry.default_text = "1"  # Texto padrão
    capacidade_entry.insert(0, capacidade_entry.default_text)
    capacidade_entry.config(foreground="gray")
    capacidade_label.pack(pady=5)
    capacidade_entry.pack(pady=5)
    capacidade_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    valor_label = tk.Label(content_quarto_frame, text="Valor do quarto:")
    valor_entry = tk.Entry(content_quarto_frame, width=50)
    valor_entry.default_text = "100.00"  # Texto padrão
    valor_entry.insert(0, valor_entry.default_text)
    valor_entry.config(foreground="gray")
    valor_label.pack(pady=5)
    valor_entry.pack(pady=5)
    valor_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    # Função para salvar os dados no banco de dados
    def save_to_database_quarto():
        try:
            numero_quarto = numero_entry.get()
            #testar se não é vazio, se é float e se ja existe
            if not numero_quarto:
                numero_entry.config(foreground="red")
                numero_entry.delete(0, "end")
                numero_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not numero_quarto.isnumeric():
                numero_entry.config(foreground="red")
                numero_entry.delete(0, "end")
                numero_entry.insert(0, "NÃO PODE CONTER LETRAS")
                return
            if utils.verifica_numero_quarto_existe(cursor, numero_quarto):
                numero_entry.config(foreground="red")
                numero_entry.delete(0, "end")
                numero_entry.insert(0, "QUARTO JÁ EXISTE")
                return
            cursor.fetchall()

            tipo_quarto = tipo_entry.get()
            if not tipo_quarto:
                tipo_entry.config(foreground="red")
                tipo_entry.delete(0, "end")
                tipo_entry.insert(0, "NÃO PODE SER NULL")
                return
            
            capacidade_quarto = capacidade_entry.get()
            if not capacidade_quarto:
                capacidade_entry.config(foreground="red")
                capacidade_entry.delete(0, "end")
                capacidade_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not capacidade_quarto.isnumeric():
                capacidade_entry.config(foreground="red")
                capacidade_entry.delete(0, "end")
                capacidade_entry.insert(0, "NÃO PODE CONTER LETRAS")
                return
            
            valor_quarto = valor_entry.get()
            if not valor_quarto:
                valor_entry.config(foreground="red")
                valor_entry.delete(0, "end")
                valor_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not valor_quarto.isnumeric():
                valor_entry.config(foreground="red")
                valor_entry.delete(0, "end")
                valor_entry.insert(0, "NÃO PODE CONTER LETRAS")
                return
            
            # Insere os dados na tabela
            cursor.execute('INSERT INTO quarto (Numero_quarto, Tipo_quarto, Capacidade_quarto, Valor_quarto) VALUES (%s, %s, %s, %s)',
                         (numero_quarto, tipo_quarto, capacidade_quarto, valor_quarto))  # Executa o comando SQL
            db.commit()  # Salva as alterações no banco de dados

            # Exibe uma mensagem de sucesso com um popup e retorna para o menu de quartos
            popup_sucesso("Quarto cadastrado com sucesso!") # Exibe uma mensagem de sucesso
            quarto_menu(tela, menu_quarto_frame, content_quarto_frame) # Retorna para o menu de quartos
            
        except Exception as e:
            popup_error(str(e))
            main_menu(tela, menu_quarto_frame, content_quarto_frame)


    salvar_button = tk.Button(content_quarto_frame, text="SALVAR", command=save_to_database_quarto)
    salvar_button.configure(bg="blue", fg="white")
    salvar_button.pack(pady=50)

#tela de buscar quarto
def buscar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame):
    #remove o menu frame
    menu_quarto_frame.pack_forget()
    #remove o conteúdo da tela
    content_quarto_frame.pack_forget()

    # cria o menu frame
    menu_quarto_frame = tk.Frame(tela, bg="gray", width=300)
    menu_quarto_frame.pack(side="left", fill="y")

    # cria o frame do conteúdo
    content_quarto_frame = tk.Frame(tela, bg="white", width=780)
    content_quarto_frame.pack(side="right", fill="both", expand=True)

    # adiciona um label ao menu_frame
    quarto_label = tk.Label(menu_quarto_frame, text="BUSCAR\nQUARTO", font=("Arial", 18))
    quarto_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_quarto_button = tk.Button(menu_quarto_frame, text="Cadastrar")
    buscar_quarto_button = tk.Button(menu_quarto_frame, text="Buscar")
    buscar_quarto_button.configure(bg="black", fg="white")
    listar_quarto_button = tk.Button(menu_quarto_frame, text="Listar")
    voltar_quarto_button = tk.Button(menu_quarto_frame, text="Voltar", command=lambda: main_menu(tela, menu_quarto_frame, content_quarto_frame))
    sair_button = tk.Button(menu_quarto_frame, text="Sair", command=tela.quit)

    # adiciona os botões ao menu
    cadastrar_quarto_button.pack(side="top", pady=10, padx=10)
    buscar_quarto_button.pack(side="top", pady=10, padx=10)
    listar_quarto_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_quarto_button.pack(side="bottom", pady=10, fill="x")

    # adiciona função dos botões
    cadastrar_quarto_button.config(command=lambda: cadastrar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame))
    listar_quarto_button.config(command=lambda: listar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame))

    # cria uma caixa de seleção com as opções de busca, CPF e nome ao lado da caixa de entrada, e abaixo um botão para buscar
    buscar_label = tk.Label(content_quarto_frame, text="Buscar por:")
    buscar_label.pack(pady=5)
    buscar_var = tk.StringVar()
    buscar_combobox = tk.ttk.Combobox(content_quarto_frame, width=12, textvariable=buscar_var, state="readonly")
    buscar_combobox["values"] = ["Número", "Tipo"]
    buscar_combobox.current(0)  # Define o valor padrão
    buscar_combobox.pack(pady=5)
    
    buscar_entry = tk.Entry(content_quarto_frame, width=50)
    buscar_entry.default_text = "123"  # Texto padrão
    buscar_entry.insert(0, buscar_entry.default_text)
    buscar_entry.config(foreground="gray")
    buscar_entry.pack(pady=5)
    buscar_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    # Função para buscar os dados no banco de dados
    def search_in_database_quarto():
        try:
            if buscar_var.get() == "Número":
                numero_quarto = buscar_entry.get()
                if not numero_quarto:
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "NÃO PODE SER NULL")
                    return
                if not numero_quarto.isnumeric():
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "NÃO PODE CONTER LETRAS")
                    return
                if not utils.verifica_numero_quarto_existe(cursor, numero_quarto):
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "QUARTO NÃO ENCONTRADO")
                    return
                cursor.fetchall()

                cursor.execute('SELECT COUNT(*) FROM quarto WHERE Numero_quarto = %s', (numero_quarto,))
                count = cursor.fetchone()[0]
                cursor.execute('SELECT * FROM quarto WHERE Numero_quarto = %s', (numero_quarto,))

                if count > 1:
                    quarto = cursor.fetchall()
                    imprimir_quarto_tabela(content_quarto_frame, quarto)
                else:
                    quarto = cursor.fetchone()
                    imprimir_quarto_editar_excluir(content_quarto_frame, quarto)

            elif buscar_var.get() == "Tipo":
                tipo_quarto = buscar_entry.get()
                if not tipo_quarto:
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "NÃO PODE SER NULL")
                    return
                if not utils.verifica_tipo_quarto_existe(cursor, tipo_quarto): 
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "TIPO NÃO ENCONTRADO")
                    return
                cursor.fetchall()

                cursor.execute('SELECT COUNT(*) FROM quarto WHERE Tipo_quarto = %s', (tipo_quarto,))
                count = cursor.fetchone()[0]
                cursor.execute('SELECT * FROM quarto WHERE Tipo_quarto = %s', (tipo_quarto,))

                if count > 1:
                    quarto = cursor.fetchall()
                    imprimir_quarto_tabela(content_quarto_frame, quarto)
                else:
                    quarto = cursor.fetchone()
                    imprimir_quarto_editar_excluir(content_quarto_frame, quarto)

        # Caso ocorra algum erro
        except Exception as e:
            popup_error(str(e))
            main_menu(tela, menu_quarto_frame, content_quarto_frame)

    buscar_button = tk.Button(content_quarto_frame, text="BUSCAR", command=search_in_database_quarto)
    buscar_button.configure(bg="blue", fg="white")
    buscar_button.pack(pady=15)

#tela de listar quarto 
def listar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame):
    # Remove the menu frame
    menu_quarto_frame.pack_forget()
    #remove o conteúdo da tela
    content_quarto_frame.pack_forget()

    # Create the menu frame on the left
    menu_quarto_frame = tk.Frame(tela, bg="gray", width=300)   # Cria um frame para o menu
    menu_quarto_frame.pack(side="left", fill="y") # Define o lado e o preenchimento do frame, y=vertical

    # cria o frame do conteúdo, frame = quadro
    content_quarto_frame = tk.Frame(tela, bg="white", width=780)
    content_quarto_frame.pack(side="right", fill="both", expand=True)

    # Adiciona um label ao menu_frame
    quarto_label = tk.Label(menu_quarto_frame, text="LISTAR\nQUARTOS", font=("Arial", 18))
    quarto_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_quarto_button = tk.Button(menu_quarto_frame, text="Cadastrar") # Cria um botão para o menu
    buscar_quarto_button = tk.Button(menu_quarto_frame, text="Buscar") # Cria um botão para o menu
    listar_quarto_button = tk.Button(menu_quarto_frame, text="Listar")  # Cria um botão para o menu
    listar_quarto_button.configure(bg="black", fg="white") # Altera a cor do botão
    voltar_quarto_button = tk.Button(menu_quarto_frame, text="Voltar", command=lambda: main_menu(tela, menu_quarto_frame, content_quarto_frame)) # Cria um botão para o menu
    sair_button = tk.Button(menu_quarto_frame, text="Sair", command=tela.quit) # Cria um botão para o menu

    # adiciona os botões ao menu
    cadastrar_quarto_button.pack(side="top", pady=10, padx=10) # Define o lado e o espaçamento do botão
    buscar_quarto_button.pack(side="top", pady=10, padx=10) #side=lado, pady=espaçamento em y, padx=espaçamento em x
    listar_quarto_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x") # Define o lado, o espaçamento e o preenchimento do botão
    voltar_quarto_button.pack(side="bottom", pady=10, fill="x") # Define o lado

    #adiciona função dos botões
    cadastrar_quarto_button.config(command=lambda: cadastrar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame)) # Define a função do botão
    buscar_quarto_button.config(command=lambda: buscar_quarto_menu(tela, menu_quarto_frame, content_quarto_frame)) # Define a função do botão

    #adicionar 3 botões no topo do content_frame para listar todos os quartos, listar quartos simples e listar quartos duplos
    listar_todos_button = tk.Button(content_quarto_frame, text="Listar todos", command=lambda: listar_todos_quartos(content_quarto_frame))
    listar_todos_button.pack(side="top", pady=10, padx=10, fill="x")

def listar_todos_quartos(content_quarto_frame):
    try:
        cursor.execute('SELECT COUNT(*) FROM quarto')
        count = cursor.fetchone()[0]

        if count < 1: # Se não houver quartos
            popup_error("Não há quartos!") # Exibe uma mensagem de erro
        else:
            cursor.fetchall() #limpa o cursor
            cursor.execute('SELECT * FROM quarto')  # Executa o comando SQL
            quarto = cursor.fetchall()  # Pega os dados do quarto
            imprimir_quarto_tabela(content_quarto_frame, quarto)

    except Exception as e:
        popup_error(str(e)) # Exibe uma mensagem de erro

def imprimir_quarto_tabela(content_quarto_frame, quarto):
    
    def sort_column(col):
        items = table.get_children('')
        items = [(table.set(item, col), item) for item in items]
        items.sort()
        for index, (value, item) in enumerate(items):
            table.move(item, '', index)

        table.heading(col, command=lambda: sort_column(col))

    table_frame = tk.Frame(content_quarto_frame, bg="white")
    table_frame.pack(pady=10)

    table = tk.ttk.Treeview(table_frame, columns=(" ", "Número", "Tipo", "Capacidade", "Valor"), show="headings", height=15)
    table.pack(side="left", fill="both", expand=True)

    table_scroll = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table_scroll.pack(side="right", fill="y")
    table.configure(yscrollcommand=table_scroll.set)

    table.heading(" ", text="ID")
    table.heading("Número", text="Número", command=lambda: sort_column("Número"))
    table.heading("Tipo", text="Tipo", command=lambda: sort_column("Tipo"))
    table.heading("Capacidade", text="Capacidade", command=lambda: sort_column("Capacidade"))
    table.heading("Valor", text="Valor", command=lambda: sort_column("Valor"))

    table.column(" ", width=40, anchor="center")
    table.column("Número", width=100, anchor="center")
    table.column("Tipo", width=100, anchor="center")
    table.column("Capacidade", width=100, anchor="center")
    table.column("Valor", width=100, anchor="center")

    i = 1
    for q in quarto:
        numero = q[0] if q[0] is not None else ""
        tipo = q[1] if q[1] is not None else ""
        capacidade = q[2] if q[2] is not None else ""
        valor = q[3] if q[3] is not None else ""

        table.insert("", "end", values=(i, numero, tipo, capacidade, valor))
        i += 1

def imprimir_quarto_editar_excluir(content_frame, quarto):

    def salvar_alteracoes_quartos():
        try:
            novo_numero_quarto = numero_entry.get()
            if not novo_numero_quarto:
                numero_entry.config(foreground="red")
                numero_entry.delete(0, "end")
                numero_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not novo_numero_quarto.isnumeric():
                numero_entry.config(foreground="red")
                numero_entry.delete(0, "end")
                numero_entry.insert(0, "NÃO PODE CONTER LETRAS")
                return
            if not utils.verifica_numero_quarto_existe(cursor, novo_numero_quarto):
                numero_entry.config(foreground="red")
                numero_entry.delete(0, "end")
                numero_entry.insert(0, "QUARTO NÃO ENCONTRADO")
                return
            cursor.fetchall()

            novo_tipo_quarto = tipo_entry.get()
            if not novo_tipo_quarto:
                tipo_entry.config(foreground="red")
                tipo_entry.delete(0, "end")
                tipo_entry.insert(0, "NÃO PODE SER NULL")
                return

            novo_capacidade_quarto = capacidade_entry.get()
            if not novo_capacidade_quarto:
                capacidade_entry.config(foreground="red")
                capacidade_entry.delete(0, "end")
                capacidade_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not novo_capacidade_quarto.isnumeric():
                capacidade_entry.config(foreground="red")
                capacidade_entry.delete(0, "end")
                capacidade_entry.insert(0, "NÃO PODE CONTER LETRAS")
                return

            novo_valor_quarto = valor_entry.get()
            if not novo_valor_quarto:
                valor_entry.config(foreground="red")
                valor_entry.delete(0, "end")
                valor_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not novo_valor_quarto.isnumeric():
                valor_entry.config(foreground="red")
                valor_entry.delete(0, "end")
                valor_entry.insert(0, "NÃO PODE CONTER LETRAS")
                return

            cursor.execute('UPDATE quarto SET Numero_quarto = %s, Tipo_quarto = %s, Capacidade_quarto = %s, Valor_quarto = %s WHERE Numero_quarto = %s',
                           (novo_numero_quarto, novo_tipo_quarto, novo_capacidade_quarto, novo_valor_quarto, quarto[0]))  # Executa o comando SQL

            db.commit()  # Salva as alterações no banco de dados

            popup_sucesso("Quarto atualizado com sucesso!")  # Exibe uma mensagem de sucesso

        except mysql.connector.Error as error:
            popup_error(str(error))

    def excluir_quarto():
        try:
            cursor.execute('DELETE FROM quarto WHERE Numero_quarto = %s', (quarto[0],))  # Executa o comando SQL
            db.commit()  # Salva as alterações no banco de dados

            popup_sucesso("Quarto excluído com sucesso!")  # Exibe uma mensagem de sucesso

        except mysql.connector.Error as error:
            popup_error(str(error))

    # Cria um novo frame para os campos de edição e exclusão
    edit_frame = tk.Frame(content_frame, bg="white")
    edit_frame.pack(pady=10)

    # preenche os campos com os dados do quarto
    numero_label = tk.Label(edit_frame, text="Número do quarto:")
    numero_entry = tk.Entry(edit_frame, width=50)
    numero_entry.insert(0, quarto[0] if quarto[0] is not None else "")
    numero_label.pack(pady=5)
    numero_entry.pack(pady=5)

    tipo_label = tk.Label(edit_frame, text="Tipo do quarto:")
    tipo_entry = tk.Entry(edit_frame, width=50)
    tipo_entry.insert(0, quarto[1] if quarto[1] is not None else "")
    tipo_label.pack(pady=5)
    tipo_entry.pack(pady=5)

    capacidade_label = tk.Label(edit_frame, text="Capacidade do quarto:")
    capacidade_entry = tk.Entry(edit_frame, width=50)
    capacidade_entry.insert(0, quarto[2] if quarto[2] is not None else "")
    capacidade_label.pack(pady=5)
    capacidade_entry.pack(pady=5)

    valor_label = tk.Label(edit_frame, text="Valor do quarto:")
    valor_entry = tk.Entry(edit_frame, width=50)
    valor_entry.insert(0, quarto[3] if quarto[3] is not None else "")
    valor_label.pack(pady=5)
    valor_entry.pack(pady=5)

    
    salvar_button = tk.Button(edit_frame, text="SALVAR", command=salvar_alteracoes_quartos)
    salvar_button.configure(bg="blue", fg="white")
    salvar_button.pack(side="left", padx=25, pady=40)

    excluir_button = tk.Button(edit_frame, text="EXCLUIR", command=excluir_quarto)
    excluir_button.configure(bg="red", fg="white")
    excluir_button.pack(side="right", padx=25, pady=40)



# SERVIÇO
#tela de menu de serviço
def servico_menu(tela, menu_servico_frame, content_servico_frame):
    # remove o menu frame
    menu_servico_frame.pack_forget()
    # remove o conteúdo da tela
    content_servico_frame.pack_forget()

    # cria o menu frame
    menu_servico_frame = tk.Frame(tela, bg="gray", width=300)
    menu_servico_frame.pack(side="left", fill="y")

    # cria o frame do conteúdo
    content_servico_frame = tk.Frame(tela, bg="white", width=780)
    content_servico_frame.pack(side="right", fill="both", expand=True)

    # adiciona um label ao menu_frame
    servico_label = tk.Label(menu_servico_frame, text="SERVIÇO", font=("Arial", 18))
    servico_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_servico_button = tk.Button(menu_servico_frame, text="Cadastrar")
    buscar_servico_button = tk.Button(menu_servico_frame, text="Buscar")
    listar_servico_button = tk.Button(menu_servico_frame, text="Listar")
    voltar_servico_button = tk.Button(menu_servico_frame, text="Voltar", command=lambda: main_menu(tela, menu_servico_frame, content_servico_frame))
    sair_button = tk.Button(menu_servico_frame, text="Sair", command=tela.quit)

    # adiciona os botões ao menu
    cadastrar_servico_button.pack(side="top", pady=10, padx=10)
    buscar_servico_button.pack(side="top", pady=10, padx=10)
    listar_servico_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_servico_button.pack(side="bottom", pady=10, fill="x")

    # adiciona função dos botões
    cadastrar_servico_button.config(command=lambda: cadastrar_servico_menu(tela, menu_servico_frame, content_servico_frame))
    buscar_servico_button.config(command=lambda: buscar_servico_menu(tela, menu_servico_frame, content_servico_frame))
    listar_servico_button.config(command=lambda: listar_servico_menu(tela, menu_servico_frame, content_servico_frame))

    #adicionar label ao content_frame
    content_label = tk.Label(content_servico_frame, text="Olimpo Hotel Management System!", font=("Helvetica", 24))
    content_label.pack(pady=50) # Define o espaçamento do label

#tela de cadastrar serviço
def cadastrar_servico_menu(tela, menu_servico_frame, content_servico_frame):
    # remove o menu frame
    menu_servico_frame.pack_forget()
    # remove o conteúdo da tela
    content_servico_frame.pack_forget()

    # cria o menu frame
    menu_servico_frame = tk.Frame(tela, bg="gray", width=300)
    menu_servico_frame.pack(side="left", fill="y")

    # cria o frame do conteúdo
    content_servico_frame = tk.Frame(tela, bg="white", width=780)
    content_servico_frame.pack(side="right", fill="both", expand=True)

    # adiciona um label ao menu_frame
    servico_label = tk.Label(menu_servico_frame, text="CADASTRAR\nSERVIÇO", font=("Arial", 18))
    servico_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_servico_button = tk.Button(menu_servico_frame, text="Cadastrar")
    cadastrar_servico_button.configure(bg="black", fg="white")
    buscar_servico_button = tk.Button(menu_servico_frame, text="Buscar")
    listar_servico_button = tk.Button(menu_servico_frame, text="Listar")
    voltar_servico_button = tk.Button(menu_servico_frame, text="Voltar", command=lambda: main_menu(tela, menu_servico_frame, content_servico_frame))
    sair_button = tk.Button(menu_servico_frame, text="Sair", command=tela.quit)

    # adiciona os botões ao menu
    cadastrar_servico_button.pack(side="top", pady=10, padx=10)
    buscar_servico_button.pack(side="top", pady=10, padx=10)
    listar_servico_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_servico_button.pack(side="bottom", pady=10, fill="x")

    # adiciona função dos botões
    buscar_servico_button.config(command=lambda: buscar_servico_menu(tela, menu_servico_frame, content_servico_frame))
    listar_servico_button.config(command=lambda: listar_servico_menu(tela, menu_servico_frame, content_servico_frame))

    # cria as caixas de entrada e rótulos para o cadastro de serviço
    nome_label = tk.Label(content_servico_frame, text="Nome do serviço:")
    nome_entry = tk.Entry(content_servico_frame, width=50)
    nome_entry.default_text = "Refeição"  # Texto padrão
    nome_entry.insert(0, nome_entry.default_text)
    nome_entry.config(foreground="gray")
    nome_label.pack(pady=5)
    nome_entry.pack(pady=5)
    nome_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    valor_label = tk.Label(content_servico_frame, text="Valor do serviço:")
    valor_entry = tk.Entry(content_servico_frame, width=50)
    valor_entry.default_text = "100.00"  # Texto padrão
    valor_entry.insert(0, valor_entry.default_text)
    valor_entry.config(foreground="gray")
    valor_label.pack(pady=5)
    valor_entry.pack(pady=5)
    valor_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    # Função para salvar os dados no banco de dados
    def save_to_database_servico():
        try:
            nome_servico = nome_entry.get()
            if not nome_servico:
                nome_entry.config(foreground="red")
                nome_entry.delete(0, "end")
                nome_entry.insert(0, "NÃO PODE SER NULL")
                return
            elif utils.servico_existe_nome(cursor, nome_servico):
                nome_entry.config(foreground="red")
                nome_entry.delete(0, "end")
                nome_entry.insert(0, "SERVIÇO JÁ EXISTE")
                return
            cursor.fetchall()
            
            valor_servico = valor_entry.get()
            if not valor_servico:
                valor_entry.config(foreground="red")
                valor_entry.delete(0, "end")
                valor_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not valor_servico.isnumeric():
                valor_entry.config(foreground="red")
                valor_entry.delete(0, "end")
                valor_entry.insert(0, "NÃO PODE CONTER LETRAS")
                return
            
            # Insere os dados na tabela
            cursor.execute('INSERT INTO servico (Nome_servico, Valor_servico) VALUES (%s, %s)',
                         (nome_servico, valor_servico))  # Executa o comando SQL
            db.commit()  # Salva as alterações no banco de dados

            # Exibe uma mensagem de sucesso com um popup e retorna para o menu de serviço
            popup_sucesso("Serviço cadastrado com sucesso!") # Exibe uma mensagem de sucesso
            servico_menu(tela, menu_servico_frame, content_servico_frame) # Retorna para o menu de serviço
            
        except Exception as e:
            popup_error(str(e))
            main_menu(tela, menu_servico_frame, content_servico_frame)


    salvar_button = tk.Button(content_servico_frame, text="SALVAR", command=save_to_database_servico)
    salvar_button.configure(bg="blue", fg="white")
    salvar_button.pack(pady=50)

#tela de buscar serviço
def buscar_servico_menu(tela, menu_servico_frame, content_servico_frame):
    #remove o menu frame
    menu_servico_frame.pack_forget()
    #remove o conteúdo da tela
    content_servico_frame.pack_forget()

    # cria o menu frame
    menu_servico_frame = tk.Frame(tela, bg="gray", width=300)
    menu_servico_frame.pack(side="left", fill="y")

    # cria o frame do conteúdo
    content_servico_frame = tk.Frame(tela, bg="white", width=780)
    content_servico_frame.pack(side="right", fill="both", expand=True)

    # adiciona um label ao menu_frame
    servico_label = tk.Label(menu_servico_frame, text="BUSCAR\nSERVIÇO", font=("Arial", 18))
    servico_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_servico_button = tk.Button(menu_servico_frame, text="Cadastrar")
    buscar_servico_button = tk.Button(menu_servico_frame, text="Buscar")
    buscar_servico_button.configure(bg="black", fg="white")
    listar_servico_button = tk.Button(menu_servico_frame, text="Listar")
    voltar_servico_button = tk.Button(menu_servico_frame, text="Voltar", command=lambda: main_menu(tela, menu_servico_frame, content_servico_frame))
    sair_button = tk.Button(menu_servico_frame, text="Sair", command=tela.quit)

    # adiciona os botões ao menu
    cadastrar_servico_button.pack(side="top", pady=10, padx=10)
    buscar_servico_button.pack(side="top", pady=10, padx=10)
    listar_servico_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_servico_button.pack(side="bottom", pady=10, fill="x")    

    # adiciona função dos botões
    cadastrar_servico_button.config(command=lambda: cadastrar_servico_menu(tela, menu_servico_frame, content_servico_frame))
    listar_servico_button.config(command=lambda: listar_servico_menu(tela, menu_servico_frame, content_servico_frame))

    # cria uma caixa de seleção com as opções de busca, CPF e nome ao lado da caixa de entrada, e abaixo um botão para buscar
    buscar_label = tk.Label(content_servico_frame, text="Buscar por:")
    buscar_label.pack(pady=5)
    buscar_var = tk.StringVar()
    buscar_combobox = tk.ttk.Combobox(content_servico_frame, width=12, textvariable=buscar_var, state="readonly")
    buscar_combobox["values"] = ["Nome", "Valor"]
    buscar_combobox.current(0)  # Define o valor padrão
    buscar_combobox.pack(pady=5)

    buscar_entry = tk.Entry(content_servico_frame, width=50)
    buscar_entry.default_text = "Refeição"  # Texto padrão
    buscar_entry.insert(0, buscar_entry.default_text)
    buscar_entry.config(foreground="gray")
    buscar_entry.pack(pady=5)
    buscar_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    # Função para buscar os dados no banco de dados
    def search_in_database_servico():
        try:
            if buscar_var.get() == "Nome":
                nome_servico = buscar_entry.get()
                if not nome_servico:
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "NÃO PODE SER NULL")
                    return
                if not utils.servico_existe_nome(cursor, nome_servico):
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "SERVIÇO NÃO ENCONTRADO")
                    return
                cursor.fetchall()

                cursor.execute('SELECT COUNT(*) FROM servico WHERE Nome_servico = %s', (nome_servico,))
                count = cursor.fetchone()[0]
                cursor.execute('SELECT * FROM servico WHERE Nome_servico = %s', (nome_servico,))

                if count > 1:
                    servico = cursor.fetchall()
                    imprimir_servico_tabela(content_servico_frame, servico)
                else:
                    servico = cursor.fetchone()
                    imprimir_servico_editar_excluir(content_servico_frame, servico)

            elif buscar_var.get() == "Valor":
                valor_servico = buscar_entry.get()
                if not valor_servico:
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "NÃO PODE SER NULL")
                    return
                if not valor_servico.isnumeric():
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "NÃO PODE CONTER LETRAS")
                    return
                if not utils.servico_existe_valor(cursor, valor_servico):
                    buscar_entry.config(foreground="red")
                    buscar_entry.delete(0, "end")
                    buscar_entry.insert(0, "SERVIÇO NÃO ENCONTRADO")
                    return
                cursor.fetchall()

                cursor.execute('SELECT COUNT(*) FROM servico WHERE Valor_servico = %s', (valor_servico,))
                count = cursor.fetchone()[0]
                cursor.execute('SELECT * FROM servico WHERE Valor_servico = %s', (valor_servico,))

                if count > 1:
                    servico = cursor.fetchall()
                    imprimir_servico_tabela(content_servico_frame, servico)
                else:
                    servico = cursor.fetchone()
                    imprimir_servico_editar_excluir(content_servico_frame, servico)

        # Caso ocorra algum erro
        except Exception as e:
            popup_error(str(e))
            main_menu(tela, menu_servico_frame, content_servico_frame)

    buscar_button = tk.Button(content_servico_frame, text="BUSCAR", command=search_in_database_servico)
    buscar_button.configure(bg="blue", fg="white")
    buscar_button.pack(pady=15)

#tela de listar serviço
def listar_servico_menu(tela, menu_servico_frame, content_servico_frame):
    # remove o menu frame
    menu_servico_frame.pack_forget()
    # remove o conteúdo da tela
    content_servico_frame.pack_forget()

    # cria o menu frame
    menu_servico_frame = tk.Frame(tela, bg="gray", width=300)
    menu_servico_frame.pack(side="left", fill="y")

    # cria o frame do conteúdo
    content_servico_frame = tk.Frame(tela, bg="white", width=780)
    content_servico_frame.pack(side="right", fill="both", expand=True)

    # adiciona um label ao menu_frame
    servico_label = tk.Label(menu_servico_frame, text="LISTAR\nSERVIÇOS", font=("Arial", 18))
    servico_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_servico_button = tk.Button(menu_servico_frame, text="Cadastrar")
    buscar_servico_button = tk.Button(menu_servico_frame, text="Buscar")
    listar_servico_button = tk.Button(menu_servico_frame, text="Listar")
    listar_servico_button.configure(bg="black", fg="white")
    voltar_servico_button = tk.Button(menu_servico_frame, text="Voltar", command=lambda: main_menu(tela, menu_servico_frame, content_servico_frame))
    sair_button = tk.Button(menu_servico_frame, text="Sair", command=tela.quit)

    # adiciona os botões ao menu
    cadastrar_servico_button.pack(side="top", pady=10, padx=10)
    buscar_servico_button.pack(side="top", pady=10, padx=10)
    listar_servico_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_servico_button.pack(side="bottom", pady=10, fill="x")

    # adiciona função dos botões
    cadastrar_servico_button.config(command=lambda: cadastrar_servico_menu(tela, menu_servico_frame, content_servico_frame))
    buscar_servico_button.config(command=lambda: buscar_servico_menu(tela, menu_servico_frame, content_servico_frame))

    #adicionar 3 botões no topo do content_frame para listar todos os serviços, listar serviços com valor menor que 100 e listar serviços com valor maior que 100
    listar_todos_button = tk.Button(content_servico_frame, text="Listar todos", command=lambda: listar_todos_servicos(content_servico_frame))
    listar_todos_button.pack(side="top", pady=10, padx=10, fill="x")

def listar_todos_servicos(content_servico_frame):
    try:
        cursor.execute('SELECT COUNT(*) FROM servico')
        count = cursor.fetchone()[0]

        if count < 1: # Se não houver serviços
            popup_error("Não há serviços!") # Exibe uma mensagem de erro
        else:
            cursor.fetchall() #limpa o cursor
            cursor.execute('SELECT * FROM servico')  # Executa o comando SQL
            servico = cursor.fetchall()  # Pega os dados do serviço
            imprimir_servico_tabela(content_servico_frame, servico)

    except Exception as e:
        popup_error(str(e)) # Exibe uma mensagem de erro

def imprimir_servico_tabela(content_servico_frame, servico):
        
        def sort_column(col):
            items = table.get_children('')
            items = [(table.set(item, col), item) for item in items]
            items.sort()
            for index, (value, item) in enumerate(items):
                table.move(item, '', index)
    
            table.heading(col, command=lambda: sort_column(col))
    
        table_frame = tk.Frame(content_servico_frame, bg="white")
        table_frame.pack(pady=10)
    
        table = tk.ttk.Treeview(table_frame, columns=(" ", "Nome", "Valor"), show="headings", height=15)
        table.pack(side="left", fill="both", expand=True)
    
        table_scroll = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table_scroll.pack(side="right", fill="y")
        table.configure(yscrollcommand=table_scroll.set)
    
        table.heading(" ", text="ID")
        table.heading("Nome", text="Nome", command=lambda: sort_column("Nome"))
        table.heading("Valor", text="Valor", command=lambda: sort_column("Valor"))
    
        table.column(" ", width=40, anchor="center")
        table.column("Nome", width=100, anchor="center")
        table.column("Valor", width=100, anchor="center")
    
        i = 1
        for s in servico:
            nome = s[0] if s[0] is not None else ""
            valor = s[1] if s[1] is not None else ""
    
            table.insert("", "end", values=(i, nome, valor))
            i += 1

def imprimir_servico_editar_excluir(content_frame, servico):
    
        def salvar_alteracoes_servicos():
            try:
                novo_nome_servico = nome_entry.get()
                if not novo_nome_servico:
                    nome_entry.config(foreground="red")
                    nome_entry.delete(0, "end")
                    nome_entry.insert(0, "NÃO PODE SER NULL")
                    return
                if not utils.servico_existe_nome(cursor, novo_nome_servico):
                    nome_entry.config(foreground="red")
                    nome_entry.delete(0, "end")
                    nome_entry.insert(0, "SERVIÇO NÃO ENCONTRADO")
                    return
                cursor.fetchall()
    
                novo_valor_servico = valor_entry.get()
                if not novo_valor_servico:
                    valor_entry.config(foreground="red")
                    valor_entry.delete(0, "end")
                    valor_entry.insert(0, "NÃO PODE SER NULL")
                    return
                if not novo_valor_servico.isnumeric():
                    valor_entry.config(foreground="red")
                    valor_entry.delete(0, "end")
                    valor_entry.insert(0, "NÃO PODE CONTER LETRAS")
                    return
    
                cursor.execute('UPDATE servico SET Nome_servico = %s, Valor_servico = %s WHERE Nome_servico = %s',
                            (novo_nome_servico, novo_valor_servico, servico[0]))  # Executa o comando SQL
    
                db.commit()  # Salva as alterações no banco de dados
    
                popup_sucesso("Serviço atualizado com sucesso!")  # Exibe uma mensagem de sucesso
    
            except mysql.connector.Error as error:
                popup_error(str(error))
    
        def excluir_servico():
            try:
                cursor.execute('DELETE FROM servico WHERE Nome_servico = %s', (servico[0],))  # Executa o comando SQL
                db.commit()  # Salva as alterações no banco de dados
    
                popup_sucesso("Serviço excluído com sucesso!")  # Exibe uma mensagem de sucesso
    
            except mysql.connector.Error as error:
                popup_error(str(error))
    
        # Cria um novo frame para os campos de edição e exclusão
        edit_frame = tk.Frame(content_frame, bg="white")
        edit_frame.pack(pady=10)
    
        # preenche os campos com os dados do serviço
        nome_label = tk.Label(edit_frame, text="Nome do serviço:")
        nome_entry = tk.Entry(edit_frame, width=50)
        nome_entry.insert(0, servico[0] if servico[0] is not None else "")
        nome_label.pack(pady=5)
        nome_entry.pack(pady=5)

        valor_label = tk.Label(edit_frame, text="Valor do serviço:")
        valor_entry = tk.Entry(edit_frame, width=50)
        valor_entry.insert(0, servico[1] if servico[1] is not None else "")
        valor_label.pack(pady=5)
        valor_entry.pack(pady=5)

        salvar_button = tk.Button(edit_frame, text="SALVAR", command=salvar_alteracoes_servicos)
        salvar_button.configure(bg="blue", fg="white")
        salvar_button.pack(side="left", padx=25, pady=40)

        excluir_button = tk.Button(edit_frame, text="EXCLUIR", command=excluir_servico)
        excluir_button.configure(bg="red", fg="white")
        excluir_button.pack(side="right", padx=25, pady=40)



# RESERVA
#tela de menu de reserva
def reserva_menu(tela, menu_reserva_frame, content_reserva_frame):
    menu_reserva_frame.pack_forget()
    content_reserva_frame.pack_forget()

    # cria o menu frame
    menu_reserva_frame = tk.Frame(tela, bg="gray", width=300)
    menu_reserva_frame.pack(side="left", fill="y")

    # cria o frame do conteúdo
    content_reserva_frame = tk.Frame(tela, bg="white", width=780)
    content_reserva_frame.pack(side="right", fill="both", expand=True)

    # adiciona um label ao menu_frame
    reserva_label = tk.Label(menu_reserva_frame, text="RESERVA", font=("Arial", 18))
    reserva_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_reserva_button = tk.Button(menu_reserva_frame, text="Cadastrar")
    buscar_reserva_button = tk.Button(menu_reserva_frame, text="Buscar")
    listar_reserva_button = tk.Button(menu_reserva_frame, text="Listar")
    voltar_reserva_button = tk.Button(menu_reserva_frame, text="Voltar", command=lambda: main_menu(tela, menu_reserva_frame, content_reserva_frame))
    sair_button = tk.Button(menu_reserva_frame, text="Sair", command=tela.quit)

    # adiciona os botões ao menu
    cadastrar_reserva_button.pack(side="top", pady=10, padx=10)
    buscar_reserva_button.pack(side="top", pady=10, padx=10)
    listar_reserva_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_reserva_button.pack(side="bottom", pady=10, fill="x")

    # adiciona função dos botões
    cadastrar_reserva_button.config(command=lambda: cadastrar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame))
    buscar_reserva_button.config(command=lambda: buscar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame))
    listar_reserva_button.config(command=lambda: listar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame))

    #adicionar label ao content_frame
    content_label = tk.Label(content_reserva_frame, text="Olimpo Hotel Management System!", font=("Helvetica", 24))
    content_label.pack(pady=50) # Define o espaçamento do label

#tela de cadastrar reserva
def cadastrar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame):
    #remove o menu frame
    menu_reserva_frame.pack_forget()
    #remove o conteúdo da tela
    content_reserva_frame.pack_forget()

    # cria o menu frame
    menu_reserva_frame = tk.Frame(tela, bg="gray", width=300)
    menu_reserva_frame.pack(side="left", fill="y")

    # cria o frame do conteúdo
    content_reserva_frame = tk.Frame(tela, bg="white", width=780)
    content_reserva_frame.pack(side="right", fill="both", expand=True)

    # adiciona um label ao menu_frame
    reserva_label = tk.Label(menu_reserva_frame, text="CADASTRAR\nRESERVA", font=("Arial", 18))
    reserva_label.pack(side="top", pady=10)

    # cria os botões do menu
    cadastrar_reserva_button = tk.Button(menu_reserva_frame, text="Cadastrar")
    cadastrar_reserva_button.configure(bg="black", fg="white")
    buscar_reserva_button = tk.Button(menu_reserva_frame, text="Buscar")
    listar_reserva_button = tk.Button(menu_reserva_frame, text="Listar")
    voltar_reserva_button = tk.Button(menu_reserva_frame, text="Voltar", command=lambda: main_menu(tela, menu_reserva_frame, content_reserva_frame))
    sair_button = tk.Button(menu_reserva_frame, text="Sair", command=tela.quit)

    # adiciona os botões ao menu
    cadastrar_reserva_button.pack(side="top", pady=10, padx=10)
    buscar_reserva_button.pack(side="top", pady=10, padx=10)    
    listar_reserva_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_reserva_button.pack(side="bottom", pady=10, fill="x")

    # adiciona função dos botões
    buscar_reserva_button.config(command=lambda: buscar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame))
    listar_reserva_button.config(command=lambda: listar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame))

    # cria as caixas de entrada e rótulos para o cadastro de reserva
    cpf_label = tk.Label(content_reserva_frame, text="CPF do cliente:")
    cpf_entry = tk.Entry(content_reserva_frame, width=50)
    cpf_entry.default_text = "12345678900"  # Texto padrão
    cpf_entry.insert(0, cpf_entry.default_text)
    cpf_entry.config(foreground="gray")
    cpf_label.pack(pady=5)
    cpf_entry.pack(pady=5)
    cpf_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    data_entrada_label = tk.Label(content_reserva_frame, text="Data de entrada:")
    data_entrada_entry = tkcalendar.DateEntry(content_reserva_frame, width=20, date_pattern="dd/mm/yyyy", background="gray", foreground="black")
    data_entrada_entry.set_date(datetime.date.today())
    data_entrada_label.pack(pady=5) # Define o espaçamento do label
    data_entrada_entry.pack(pady=5)

    data_saida_label = tk.Label(content_reserva_frame, text="Data de saída:")
    data_saida_entry = tkcalendar.DateEntry(content_reserva_frame, width=20, date_pattern="dd/mm/yyyy", background="gray", foreground="black")
    data_saida_entry.set_date(datetime.date.today() + datetime.timedelta(days=1))
    data_saida_label.pack(pady=5)
    data_saida_entry.pack(pady=5)

    quarto_label = tk.Label(content_reserva_frame, text="Quarto:")
    quarto_entry = tk.Entry(content_reserva_frame, width=50)
    quarto_entry.default_text = "123"  # Texto padrão
    quarto_entry.insert(0, quarto_entry.default_text)
    quarto_entry.config(foreground="gray")
    quarto_label.pack(pady=5)
    quarto_entry.pack(pady=5)
    quarto_entry.bind("<FocusIn>", clear_text) # Limpa o texto padrão da caixa de entrada quando ela recebe o foco

    # Função para salvar os dados no banco de dados
    def save_to_database_reserva():
        try:
            cpf_cliente = cpf_entry.get()
            if not utils.validar_cpf(cpf_cliente):
                cpf_entry.config(foreground="red")
                cpf_entry.delete(0, "end")
                cpf_entry.insert(0, "CPF INVÁLIDO")
                return
            elif not utils.cpf_existe(cursor, cpf_cliente):
                cpf_entry.config(foreground="red")
                cpf_entry.delete(0, "end")
                cpf_entry.insert(0, "CLIENTE NÃO EXISTE")
                return
            cursor.fetchall()

            data_entrada = data_entrada_entry.get_date()
            if not data_entrada:
                data_entrada_entry.config(foreground="red")
                data_entrada_entry.delete(0, "end")
                data_entrada_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not utils.validar_data(data_entrada):
                data_entrada_entry.config(foreground="red")
                data_entrada_entry.delete(0, "end")
                data_entrada_entry.insert(0, "DATA INVÁLIDA")
                return
            
            data_saida = data_saida_entry.get_date()
            if not data_saida:
                data_saida_entry.config(foreground="red")
                data_saida_entry.delete(0, "end")
                data_saida_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not utils.validar_data(data_saida):
                data_saida_entry.config(foreground="red")
                data_saida_entry.delete(0, "end")
                data_saida_entry.insert(0, "DATA INVÁLIDA")
                return
            
            if data_entrada >= data_saida:
                data_entrada_entry.config(foreground="red")
                data_entrada_entry.delete(0, "end")
                data_entrada_entry.insert(0, "DATA DE ENTRADA MAIOR/IGUAL QUE DATA DE SAÍDA")
                return
            
            quarto = quarto_entry.get()
            if not quarto:
                quarto_entry.config(foreground="red")
                quarto_entry.delete(0, "end")
                quarto_entry.insert(0, "NÃO PODE SER NULL")
                return
            if not quarto.isnumeric():
                quarto_entry.config(foreground="red")
                quarto_entry.delete(0, "end")
                quarto_entry.insert(0, "NÃO PODE CONTER LETRAS")
                return
            if not utils.verifica_numero_quarto_existe(cursor, quarto):
                quarto_entry.config(foreground="red")
                quarto_entry.delete(0, "end")
                quarto_entry.insert(0, "QUARTO NÃO EXISTE")
                return
            cursor.fetchall()
            
            #verificar se o quarto está disponível entre as datas de check-in e check-out
            cursor.execute('SELECT * FROM RESERVA R, ALOCA A WHERE ((R.ID_reserva = A.ID_reserva) AND (A.Numero_quarto = %s AND (R.Data_check_out_reserva >= %s AND (R.Data_check_in_reserva <= %s AND R.Data_check_out_reserva >= %s))))',
                                           (quarto, data_entrada, data_saida, data_saida))
            if cursor.fetchone() is not None:
                popup_error("Quarto indisponível entre as datas de check-in e check-out!")
                return
            cursor.fetchall()

            cursor.execute('SELECT * FROM RESERVA R, ALOCA A WHERE (R.ID_reserva = A.ID_reserva AND A.Numero_quarto = %s AND ((R.Data_check_in_reserva <= %s AND R.Data_check_out_reserva >= %s) AND R.Data_check_in_reserva <= %s ))',
                                           (quarto, data_entrada, data_entrada, data_saida))
            if cursor.fetchone() is not None:
                popup_error("Quarto indisponível entre as datas de check-in e check-out!")
                return
            cursor.fetchall()


            # Insere os dados na tabela reserva
            cursor.execute('INSERT INTO reserva (Data_check_in_reserva, Data_check_out_reserva, CLIENTE) VALUES (%s, %s, %s)',
                            (data_entrada, data_saida, cpf_cliente))  # Executa o comando SQL
            # Insere os dados na tabela ALOCA
            cursor.execute('INSERT INTO aloca (Numero_quarto, ID_reserva) VALUES (%s, %s)',
                            (quarto, cursor.lastrowid))  # Executa o comando SQL
            db.commit()  # Salva as alterações no banco de dados

            # Exibe uma mensagem de sucesso com um popup e retorna para o menu de reserva
            popup_sucesso("Reserva cadastrada com sucesso!") # Exibe uma mensagem de sucesso
            reserva_menu(tela, menu_reserva_frame, content_reserva_frame) # Retorna para o menu de reserva
            
        except Exception as e:
            popup_error(str(e))
            main_menu(tela, menu_reserva_frame, content_reserva_frame)

    salvar_button = tk.Button(content_reserva_frame, text="SALVAR", command=save_to_database_reserva)
    salvar_button.configure(bg="blue", fg="white")
    salvar_button.pack(pady=50)

# Função de menu de impressão de reserva
def listar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame):
    menu_reserva_frame.pack_forget() # Apaga o menu de reserva
    content_reserva_frame.pack_forget() # Apaga o conteúdo da reserva

    # Cria um frame para o conteúdo da página
    menu_reserva_frame = tk.Frame(tela, bg="gray", width=300)
    menu_reserva_frame.pack(side="left", fill="y")

    # Cria um frame para o conteúdo da página
    content_reserva_frame = tk.Frame(tela, bg="white", width=780)
    content_reserva_frame.pack(side="right", fill="both", expand=True)

    #adiciona um label ao menu frame
    reserva_label = tk.Label(menu_reserva_frame, text="LISTAR\nRESERVAS", font=("Arial", 18))
    reserva_label.pack(side="top", pady=10)

    #cria os botoes do menu
    cadastrar_reserva_button = tk.Button(menu_reserva_frame, text="CADASTRAR")
    buscar_reserva_button = tk.Button(menu_reserva_frame, text="BUSCAR")
    listar_reserva_button = tk.Button(menu_reserva_frame, text="LISTAR")
    listar_reserva_button.configure(bg="black", fg="white")
    voltar_reserva_button = tk.Button(menu_reserva_frame, text="VOLTAR", command=lambda: main_menu(tela, menu_reserva_frame, content_reserva_frame))
    sair_button = tk.Button(menu_reserva_frame, text="SAIR", command=tela.quit)

    #adiciona os botoes ao menu frame
    cadastrar_reserva_button.pack(side="top", pady=10, padx=10)
    buscar_reserva_button.pack(side="top", pady=10, padx=10)
    listar_reserva_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_reserva_button.pack(side="bottom", pady=10, fill="x")

    #adiciona funcionalidade aos botoes
    cadastrar_reserva_button.configure(command=lambda: cadastrar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame))
    buscar_reserva_button.configure(command=lambda: buscar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame))

    #adiciona botoes no content frame
    listar_todas_reservas_button = tk.Button(content_reserva_frame, text="LISTAR TODAS AS RESERVAS", command=lambda: listar_todas_reservas(content_reserva_frame))
    listar_todas_reservas_button.pack(side="top", pady=10, padx=10, fill="x")

    listar_reservas_atuais_button = tk.Button(content_reserva_frame, text="LISTAR RESERVAS ATUAIS", command=lambda: listar_reservas_atuais(content_reserva_frame))
    listar_reservas_atuais_button.pack(side="top", pady=10, padx=10, fill="x")

    listar_reservas_cliente_button = tk.Button(content_reserva_frame, text="LISTAR RESERVAS DE UM CLIENTE", command=lambda: listar_reservas_cliente(content_reserva_frame))
    listar_reservas_cliente_button.pack(side="top", pady=10, padx=10, fill="x")

    listar_reservas_quarto_button = tk.Button(content_reserva_frame, text="LISTAR RESERVAS DE UM QUARTO", command=lambda: listar_reservas_por_quarto(content_reserva_frame))
    listar_reservas_quarto_button.pack(side="top", pady=10, padx=10, fill="x")

    listar_reservas_servico_button = tk.Button(content_reserva_frame, text="LISTAR RESERVAS COM USO DE SERVIÇO", command=lambda: listar_reservas_servico(content_reserva_frame))
    listar_reservas_servico_button.pack(side="top", pady=10, padx=10, fill="x")

def buscar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame):
    menu_reserva_frame.pack_forget() # Apaga o menu de reserva
    content_reserva_frame.pack_forget() # Apaga o conteúdo da reserva

    # Cria um frame para o conteúdo da página
    menu_reserva_frame = tk.Frame(tela, bg="gray", width=300)
    menu_reserva_frame.pack(side="left", fill="y")

    # Cria um frame para o conteúdo da página
    content_reserva_frame = tk.Frame(tela, bg="white", width=780)
    content_reserva_frame.pack(side="right", fill="both", expand=True)

    #adiciona um label ao menu frame
    reserva_label = tk.Label(menu_reserva_frame, text="BUSCAR\nRESERVAS", font=("Arial", 18))
    reserva_label.pack(side="top", pady=10)

    #cria os botoes do menu
    cadastrar_reserva_button = tk.Button(menu_reserva_frame, text="CADASTRAR")
    buscar_reserva_button = tk.Button(menu_reserva_frame, text="BUSCAR")
    buscar_reserva_button.configure(bg="black", fg="white")
    listar_reserva_button = tk.Button(menu_reserva_frame, text="LISTAR")
    voltar_reserva_button = tk.Button(menu_reserva_frame, text="VOLTAR", command=lambda: main_menu(tela, menu_reserva_frame, content_reserva_frame))
    sair_button = tk.Button(menu_reserva_frame, text="SAIR", command=tela.quit)

    #adiciona os botoes ao menu frame
    cadastrar_reserva_button.pack(side="top", pady=10, padx=10)
    buscar_reserva_button.pack(side="top", pady=10, padx=10)
    listar_reserva_button.pack(side="top", pady=10, padx=10)
    sair_button.pack(side="bottom", pady=10, fill="x")
    voltar_reserva_button.pack(side="bottom", pady=10, fill="x")

    #adiciona funcionalidade aos botoes
    cadastrar_reserva_button.configure(command=lambda: cadastrar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame))
    listar_reserva_button.configure(command=lambda: listar_reserva_menu(tela, menu_reserva_frame, content_reserva_frame))

    buscar_label = tk.Label(content_reserva_frame, text="BUSCAR POR:")
    buscar_label.pack(pady=5) # Adiciona o label na tela
    buscar_var = tk.StringVar()
    buscar_combobox = tk.ttk.Combobox(content_reserva_frame, width=20, textvariable=buscar_var, state="readonly")
    buscar_combobox["values"] = ["CPF", "DATA", "ID DA RESERVA"]
    buscar_combobox.current(0)  # Define o valor padrão
    buscar_combobox.pack(pady=5) # Adiciona o combobox na tela

    buscar_entry = tk.Entry(content_reserva_frame, width=50)
    buscar_entry.default_text = "Digite o CPF, a data ou o ID da reserva"
    buscar_entry.insert(0, buscar_entry.default_text)
    buscar_entry.configure(fg="gray")
    buscar_entry.pack(pady=5)
    buscar_entry.bind("<FocusIn>", clear_text)

    #função para buscar a reserva no banco de dados
    def buscar_reserva_in_database():
        try:
            if buscar_var.get() == "CPF":
                cpf_cliente = buscar_entry.get()
                if cpf_cliente == "" or cpf_cliente == buscar_entry.default_text:
                    popup_error("Digite o CPF do cliente")
                elif not utils.validar_cpf(cpf_cliente):
                    popup_error("CPF inválido")
                elif not utils.cpf_existe(cursor, cpf_cliente):
                    popup_error("CPF não cadastrado")
                else:
                    reservas = utils.buscar_reserva_por_cpf(cursor, cpf_cliente)
                    if reservas == []:
                        popup_error("Cliente não possui reservas")
                    else:
                        cursor.fetchall()

                        cursor.execute('SELECT COUNT(*) FROM RESERVA R, ALOCA A, CLIENTE C WHERE R.ID_reserva = A.ID_reserva AND R.CLIENTE = C.CPF AND R.CLIENTE = %s', (cpf_cliente,))
                        count = cursor.fetchone()[0]
                        cursor.execute('SELECT R.ID_reserva, R.Data_check_in_reserva, R.Data_check_out_reserva, C.CPF, C.Nome_cliente, A.Numero_quarto FROM RESERVA R, ALOCA A, CLIENTE C WHERE R.ID_reserva = A.ID_reserva AND R.CLIENTE = C.CPF AND R.CLIENTE = %s', (cpf_cliente,))
                        if count == 1:
                            reserva = cursor.fetchone()
                            imprimir_reservas_editar_excluir(content_reserva_frame, reserva)
                        else:
                            reserva = cursor.fetchall()
                            imprimir_reserva_tabela(content_reserva_frame, reserva)

            elif buscar_var.get() == "DATA":
                data = buscar_entry.get()
                if data == "" or data == buscar_entry.default_text:
                    popup_error("Digite a data da reserva")
                elif not utils.validar_data(data):
                    popup_error("Data inválida")
                else:
                    reservas = utils.buscar_reserva_por_data(cursor, data)
                    if reservas == []:
                        popup_error("Não há reservas para essa data")
                    else:
                        cursor.fetchall()

                        cursor.execute('SELECT COUNT(*) FROM RESERVA R, ALOCA A, CLIENTE C WHERE C.CPF = R.CLIENTE AND R.ID_reserva = A.ID_reserva AND R.Data_check_in_reserva <= %s AND R.Data_check_out_reserva >= %s', (data, data))
                        count = cursor.fetchone()[0]
                        cursor.execute('SELECT R.ID_reserva, R.Data_check_in_reserva, R.Data_check_out_reserva, C.CPF, C.Nome_cliente, A.Numero_quarto FROM RESERVA R, ALOCA A, CLIENTE C WHERE C.CPF = R.CLIENTE AND R.ID_reserva = A.ID_reserva AND R.Data_check_in_reserva <= %s AND R.Data_check_out_reserva >= %s', (data, data))

                        if count == 1:
                            reserva = cursor.fetchone()
                            imprimir_reservas_editar_excluir(content_reserva_frame, reserva)
                        else:
                            reserva = cursor.fetchall()
                            imprimir_reserva_tabela(content_reserva_frame, reserva)

            elif buscar_var.get() == "ID DA RESERVA":
                id_reserva = buscar_entry.get()
                if id_reserva == "" or id_reserva == buscar_entry.default_text:
                    popup_error("Digite o ID da reserva")
                elif not utils.reserva_existe(cursor, id_reserva):
                    popup_error("ID da reserva não existe")
                else:
                    cursor.execute('SELECT R.ID_reserva, R.Data_check_in_reserva, R.Data_check_out_reserva, C.CPF, C.Nome_cliente, A.Numero_quarto FROM RESERVA R, ALOCA A, CLIENTE C WHERE C.CPF = R.CLIENTE AND R.ID_reserva = A.ID_reserva AND R.ID_reserva = %s', (id_reserva,))
                    reserva = cursor.fetchone()
                    imprimir_reservas_editar_excluir(content_reserva_frame, reserva)

        except Exception as e:
            popup_error(str(e))
            main_menu(tela, menu_reserva_frame, content_reserva_frame)

    #adiciona um botao para buscar a reserva
    buscar_button = tk.Button(content_reserva_frame, text="BUSCAR", command=buscar_reserva_in_database)
    buscar_button.configure(bg="blue", fg="white")
    buscar_button.pack(pady=5)

#função para listar as reservas em uma tabela
def imprimir_reserva_tabela(content_reserva_frame, reserva):
    def sort_column(col):
        items = table.get_children('')
        items = [(table.set(item, col), item) for item in items]
        items.sort()
        for index, (value, item) in enumerate(items):
            table.move(item, '', index)

        table.heading(col, command=lambda: sort_column(col))

    table_frame = tk.Frame(content_reserva_frame, bg="white")
    table_frame.pack(pady=10)

    table = tk.ttk.Treeview(table_frame, columns=("ID_reserva", "Data_check_in_reserva", "Data_check_out_reserva", "CPF", "Nome", "Numero_quarto"), 
                            show="headings", height="15")
    table.pack(side="left", fill="both", expand=True)

    table_scroll = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table_scroll.pack(side="right", fill="y")
    table.configure(yscrollcommand=table_scroll.set)

    table.heading("ID_reserva", text="ID_reserva", command=lambda: sort_column("ID_reserva"))
    table.heading("Data_check_in_reserva", text="Data_check_in_reserva", command=lambda: sort_column("Data_check_in_reserva"))
    table.heading("Data_check_out_reserva", text="Data_check_out_reserva", command=lambda: sort_column("Data_check_out_reserva"))
    table.heading("CPF", text="CPF", command=lambda: sort_column("CPF"))
    table.heading("Nome", text="Nome", command=lambda: sort_column("Nome"))
    table.heading("Numero_quarto", text="Numero_quarto", command=lambda: sort_column("Numero_quarto"))

    #ajusta a largura das colunas manualmente
    table.column("ID_reserva", width=90, anchor="center")
    table.column("Data_check_in_reserva", width=150, anchor="center")
    table.column("Data_check_out_reserva", width=150, anchor="center")
    table.column("CPF", width=100, anchor="center")
    table.column("Nome", width=150, anchor="center")
    table.column("Numero_quarto", width=100, anchor="center")

    for r in reserva:
        id = r[0] if r[0] is not None else ""
        data_check_in = r[1] if r[1] is not None else ""
        data_check_out = r[2] if r[2] is not None else ""
        cpf = r[3] if r[3] is not None else ""
        nome = r[4] if r[4] is not None else ""
        numero_quarto = r[5] if r[5] is not None else ""

        table.insert("", "end", values=(id, data_check_in, data_check_out, cpf, nome, numero_quarto))

def imprimir_reservas_editar_excluir(content_reserva_frame, reserva):

    def salvar_alteracoes_reservas():
        try:
            nova_data_check_in = data_check_in_entry.get_date()
            if nova_data_check_in == "":
                popup_error("Digite a nova data de check-in da reserva")
            elif not utils.validar_data(nova_data_check_in):
                popup_error("Data de check-in inválida")
            
            nova_data_check_out = data_check_out_entry.get_date()
            if nova_data_check_out == "":
                popup_error("Digite a nova data de check-out da reserva")
            elif not utils.validar_data(nova_data_check_out):
                popup_error("Data de check-out inválida")
            
            novo_quarto = numero_quarto_entry.get()
            if novo_quarto == "":
                popup_error("Digite o novo número do quarto da reserva")
            elif not utils.verifica_numero_quarto_existe(cursor, novo_quarto):
                popup_error("Número de quarto inválido")
            cursor.fetchall() # limpa o cursor

            cursor.execute('UPDATE RESERVA SET Data_check_in_reserva = %s, Data_check_out_reserva = %s WHERE ID_reserva = %s',
                            (nova_data_check_in, nova_data_check_out, reserva[0]))
            cursor.execute('UPDATE ALOCA SET Numero_quarto = %s WHERE ID_reserva = %s',
                            (novo_quarto, reserva[0]))
            db.commit()

            popup_sucesso("Reserva atualizada com sucesso")

        except mysql.connector.Error as error:
            popup_error(str(error))

    def excluir_reserva():
        try:
            cursor.execute('DELETE FROM RESERVA WHERE ID_reserva = %s', (reserva[0],))
            db.commit()

            popup_sucesso("Reserva excluída com sucesso")

        except mysql.connector.Error as error:
            popup_error(str(error))

    # Cria um novo frame para os campos de edição e exclusão
    edit_frame = tk.Frame(content_reserva_frame, bg="white")
    edit_frame.pack(pady=10)

    # Preencha os campos de edição com os valores da reserva, mantendo as caixas vazias para valores nulos
    #id_reserva não pode ser editado
    id_reserva_label = tk.Label(edit_frame, text="ID: ")
    id_reserva_entry = tk.Entry(edit_frame, width=30)
    id_reserva_entry.insert(0, reserva[0] if reserva[0] is not None else "")
    id_reserva_entry.configure(state="readonly")
    id_reserva_label.pack(pady=5)
    id_reserva_entry.pack(pady=5)

    data_check_in_label = tk.Label(edit_frame, text="Data de Entrada: ")
    data_check_in_entry = tkcalendar.DateEntry(edit_frame, width=12, date_pattern='yyyy/mm/dd', background="gray", foreground="black")
    data_check_in_entry.set_date(reserva[1] if reserva[1] is not None else "")
    data_check_in_entry.pack(pady=5)
    data_check_in_label.pack(pady=5)

    data_check_out_label = tk.Label(edit_frame, text="Data de Saída: ")
    data_check_out_entry = tkcalendar.DateEntry(edit_frame, width=12, date_pattern='yyyy/mm/dd', background="gray", foreground="black")
    data_check_out_entry.set_date(reserva[2] if reserva[2] is not None else "")
    data_check_out_entry.pack(pady=5)
    data_check_out_label.pack(pady=5)

    cpf_label = tk.Label(edit_frame, text="CPF: ")
    cpf_entry = tk.Entry(edit_frame, width=30)
    cpf_entry.insert(0, reserva[3] if reserva[3] is not None else "")
    cpf_entry.configure(state="readonly")
    cpf_label.pack(pady=5)
    cpf_entry.pack(pady=5)

    nome_label = tk.Label(edit_frame, text="Nome: ")
    nome_entry = tk.Entry(edit_frame, width=30)
    nome_entry.insert(0, reserva[4] if reserva[4] is not None else "")
    nome_entry.configure(state="readonly")
    nome_label.pack(pady=5)
    nome_entry.pack(pady=5)

    numero_quarto_label = tk.Label(edit_frame, text="Número do Quarto: ")
    numero_quarto_entry = tk.Entry(edit_frame, width=30)
    numero_quarto_entry.insert(0, reserva[5] if reserva[5] is not None else "")
    numero_quarto_label.pack(pady=5)
    numero_quarto_entry.pack(pady=5)

    # Cria um botão para salvar as alterações
    salvar_button = tk.Button(edit_frame, text="Salvar Alterações", command=salvar_alteracoes_reservas)
    salvar_button.configure(bg="green", fg="white")
    salvar_button.pack(side="left", padx=25, pady=40)

    # Adicione um botão para excluir a reserva
    excluir_button = tk.Button(edit_frame, text="Excluir", command=excluir_reserva)
    excluir_button.configure(bg="red", fg="white")
    excluir_button.pack(side="right", padx=25, pady=40)

def listar_todas_reservas(content_frame):
    try:
        cursor.execute('SELECT COUNT(*) FROM RESERVA')
        count = cursor.fetchone()[0]

        if count <1:
            popup_error("Não há reservas cadastradas")
            return
        else:
            cursor.execute('SELECT R.ID_reserva, R.Data_check_in_reserva, R.Data_check_out_reserva, C.CPF, C.Nome_cliente, A.Numero_quarto FROM RESERVA R, ALOCA A, CLIENTE C WHERE C.CPF = R.CLIENTE AND R.ID_reserva = A.ID_reserva')
            reserva = cursor.fetchall()
            imprimir_reserva_tabela(content_frame, reserva)

    except mysql.connector.Error as error:
        popup_error(str(error))

def listar_reservas_atuais(content_frame):
    try:
        cursor.execute('SELECT COUNT(*) FROM RESERVA WHERE Data_check_out_reserva > CURDATE()')
        count = cursor.fetchone()[0]

        if count <1:
            popup_error("Não há reservas atuais")
            return
        else:
            cursor.execute('SELECT R.ID_reserva, R.Data_check_in_reserva, R.Data_check_out_reserva, C.CPF, C.Nome_cliente, A.Numero_quarto FROM RESERVA R, ALOCA A, CLIENTE C WHERE C.CPF = R.CLIENTE AND R.ID_reserva = A.ID_reserva AND R.Data_check_out_reserva > CURDATE() AND R.Data_check_in_reserva < CURDATE()')
            reserva = cursor.fetchall()
            imprimir_reserva_tabela(content_frame, reserva)

    except mysql.connector.Error as error:
        popup_error(str(error))

def listar_reservas_cliente(content_frame):
    try:
        cpf_label = tk.Label(content_frame, text="CPF: ")
        cpf_entry = tk.Entry(content_frame, width=50)
        cpf_entry.default_text = '12345678900'
        cpf_entry.insert(0, cpf_entry.default_text)
        cpf_entry.config(foreground="gray")
        cpf_label.pack(pady=5)
        cpf_entry.pack(pady=5)
        cpf_entry.bind("<FocusIn>", clear_text)

        imprimir_button = tk.Button(content_frame, text="Imprimir", command=lambda: imprimir_reservas_por_cliente(content_frame))
        imprimir_button.configure(bg="blue", fg="white")
        imprimir_button.pack(pady=10)

        def imprimir_reservas_por_cliente(content_frame):

            cpf = cpf_entry.get()
            if cpf == cpf_entry.default_text or cpf == "":
                popup_error("Digite um CPF válido")
                return
            if not utils.validar_cpf(cpf):
                popup_error("Digite um CPF válido")
                return
            if not utils.cpf_existe(cursor, cpf):
                popup_error("CPF não cadastrado")
                return
                        
            cursor.execute('SELECT COUNT(*) FROM RESERVA WHERE CLIENTE = %s', (cpf,))
            count = cursor.fetchone()[0]

            if count <1:
                popup_error("Não há reservas para esse cliente")
                return
            else:
                cursor.execute('SELECT R.ID_reserva, R.Data_check_in_reserva, R.Data_check_out_reserva, C.CPF, C.Nome_cliente, A.Numero_quarto FROM RESERVA R, ALOCA A, CLIENTE C WHERE C.CPF = R.CLIENTE AND R.ID_reserva = A.ID_reserva AND R.CLIENTE = %s', (cpf,))
                reserva = cursor.fetchall()
                imprimir_reserva_tabela(content_frame, reserva)

    except mysql.connector.Error as error:
        popup_error(str(error))

def listar_reservas_por_quarto(content_frame):
    try:
        numero_quarto_label = tk.Label(content_frame, text="Número do Quarto: ")
        numero_quarto_entry = tk.Entry(content_frame, width=50)
        numero_quarto_entry.default_text = '123'
        numero_quarto_entry.insert(0, numero_quarto_entry.default_text)
        numero_quarto_entry.config(foreground="gray")
        numero_quarto_label.pack(pady=5)
        numero_quarto_entry.pack(pady=5)
        numero_quarto_entry.bind("<FocusIn>", clear_text)

        imprimir_button = tk.Button(content_frame, text="Imprimir", command=lambda: imprimir_reservas_por_quarto(content_frame))
        imprimir_button.configure(bg="blue", fg="white")
        imprimir_button.pack(pady=10)

        def imprimir_reservas_por_quarto(content_frame):

            numero_quarto = numero_quarto_entry.get()
            if numero_quarto == numero_quarto_entry.default_text or numero_quarto == "":
                popup_error("Digite um número de quarto válido")
                return
            if not utils.verifica_numero_quarto_existe(cursor, numero_quarto):
                popup_error("Número de quarto não cadastrado")
                return
                        
            cursor.execute('SELECT COUNT(*) FROM RESERVA WHERE ID_reserva IN (SELECT ID_reserva FROM ALOCA WHERE Numero_quarto = %s)', (numero_quarto,))
            count = cursor.fetchone()[0]

            if count <1:
                popup_error("Não há reservas para esse quarto")
                return
            else:
                cursor.execute('SELECT R.ID_reserva, R.Data_check_in_reserva, R.Data_check_out_reserva, C.CPF, C.Nome_cliente, A.Numero_quarto FROM RESERVA R, ALOCA A, CLIENTE C WHERE C.CPF = R.CLIENTE AND R.ID_reserva = A.ID_reserva AND A.Numero_quarto = %s', (numero_quarto,))
                reserva = cursor.fetchall()
                imprimir_reserva_tabela(content_frame, reserva)

    except mysql.connector.Error as error:
        popup_error(str(error))

def listar_reservas_servico(content_frame):
    try:
        cursor.execute('SELECT COUNT(*) FROM RESERVA R, POSSUI P WHERE R.ID_reserva = P.ID_reserva AND P.Nome_servico IS NOT NULL')
        count = cursor.fetchone()[0]

        if count <1:
            popup_error("Não há reservas com serviços")
            return
        else:
            cursor.execute('SELECT R.ID_reserva, R.Data_check_in_reserva, R.Data_check_out_reserva, C.CPF, C.Nome_cliente, A.Numero_quarto, P.Nome_servico, P.Quantidade_servico FROM RESERVA R, ALOCA A, CLIENTE C, POSSUI P WHERE C.CPF = R.CLIENTE AND R.ID_reserva = A.ID_reserva AND R.ID_reserva = P.ID_reserva AND P.Nome_servico IS NOT NULL')
            reserva = cursor.fetchall()

            imprimir_reserva_servico_tabela(content_frame, reserva)

    except mysql.connector.Error as error:
        popup_error(str(error))

def imprimir_reserva_servico_tabela(content_reserva_frame, reserva):

    def sort_column(col):
        items = table.get_children('')
        items = [(table.set(item, col), item) for item in items]
        items.sort()
        for index, (value, item) in enumerate(items):
            table.move(item, '', index)

        table.heading(col, command=lambda: sort_column(col))

    table_frame = tk.Frame(content_reserva_frame, bg="white")
    table_frame.pack(pady=10)

    table = tk.ttk.Treeview(table_frame, columns=("ID_reserva", "Data_check_in_reserva", "Data_check_out_reserva", "CPF", "Nome", "Numero_quarto", "Nome_servico", "Quantidade_servico"), show="headings", height="15")
    table.pack(side="left", fill="both", expand=True)

    table_scroll = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table_scroll.pack(side="right", fill="y")
    table.configure(yscrollcommand=table_scroll.set)

    table.heading("ID_reserva", text="ID_reserva", anchor="center", command=lambda: sort_column("ID_reserva"))
    table.heading("Data_check_in_reserva", text="Data_check_in_reserva", anchor="center", command=lambda: sort_column("Data_check_in_reserva"))
    table.heading("Data_check_out_reserva", text="Data_check_out_reserva", anchor="center", command=lambda: sort_column("Data_check_out_reserva"))
    table.heading("CPF", text="CPF", anchor="center", command=lambda: sort_column("CPF"))
    table.heading("Nome", text="Nome", anchor="center", command=lambda: sort_column("Nome"))
    table.heading("Numero_quarto", text="Numero_quarto", anchor="center", command=lambda: sort_column("Numero_quarto"))
    table.heading("Nome_servico", text="Nome_servico", anchor="center", command=lambda: sort_column("Nome_servico"))
    table.heading("Quantidade_servico", text="Quantidade_servico", anchor="center", command=lambda: sort_column("Quantidade_servico"))

    table.column("ID_reserva", width=90, anchor="center")
    table.column("Data_check_in_reserva", width=150, anchor="center")
    table.column("Data_check_out_reserva", width=150, anchor="center")
    table.column("CPF", width=100, anchor="center")
    table.column("Nome", width=150, anchor="center")
    table.column("Numero_quarto", width=100, anchor="center")
    table.column("Nome_servico", width=100, anchor="center")
    table.column("Quantidade_servico", width=700, anchor="center")

    for i in reserva:
        id = i[0] if i[0] is not None else ""
        data_check_in = i[1] if i[1] is not None else ""
        data_check_out = i[2] if i[2] is not None else ""
        cpf = i[3] if i[3] is not None else ""
        nome = i[4] if i[4] is not None else ""
        numero_quarto = i[5] if i[5] is not None else ""
        nome_servico = i[6] if i[6] is not None else ""
        quantidade_servico = i[7] if i[7] is not None else ""

        table.insert("", "end", values=(id, data_check_in, data_check_out, cpf, nome, numero_quarto, nome_servico, quantidade_servico))

# Start the main menu
main_menu()