"Sistema de Reservas de Hotel"


Entidades Principais:

Clientes: Armazene informações sobre os clientes, como nome, endereço, número de telefone, endereço de e-mail, etc. Cada cliente terá um identificador único que será o CPF.

Quartos: Mantenha os detalhes dos quartos disponíveis, como número do quarto, tipo (individual, duplo, suíte, etc.), capacidade, preço, etc. Cada quarto também terá um identificador único que será o número do mesmo.

Reservas: Registre as reservas feitas pelos clientes, incluindo informações como data de check-in, data de check-out, número de pessoas, número do quarto reservado, informações do cliente associado à reserva, etc. Cada reserva terá um identificador único.


Relacionamentos:

Um cliente pode fazer várias reservas (relação um para muitos entre Clientes e Reservas).
Cada reserva está associada a um quarto específico (relação um para um entre Reservas e Quartos).


Funcionalidades Adicionais:

Verificação de Disponibilidade: O banco de dados pode ser usado para verificar a disponibilidade de quartos em determinadas datas. Isso pode envolver a consulta das reservas existentes para verificar quais quartos estão ocupados em um determinado período.
Relatórios e Estatísticas: O banco de dados pode ser usado para gerar relatórios e estatísticas relacionados às reservas, como o número de reservas por período, taxa de ocupação dos quartos, receita gerada, etc.


Interface de Usuário:

O banco de dados pode ser integrado a uma interface de usuário, como um  aplicativo desktop desenvolvido em python, para facilitar a interação dos funcionários do hotel com o sistema de reservas. Através dessa interface, os funcionários podem realizar operações como criação de reservas, consulta de disponibilidade, visualização de relatórios, etc.
