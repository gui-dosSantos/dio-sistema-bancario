from datetime import datetime

MENU = f'''
{' MENU '.center(20, '-')}

[1] Depósito
[2] Saque
[3] Extrato
[0] Sair

'''
usuarios = [{'nome': 'Test', 'data_nascimento': '01/01/1900', 'cpf': '00000000000', 'endereco': 'Rua Teste, 0 - Bairro - Cidade/ES', 'ativo': True}]
contas = []
saldo = 0
saques_realizados_hoje = 0
MAX_TENTATIVAS = 3
LIMITE_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3
EXTRATO_INICIO = f"{' EXTRATO '.center(20, '-')}\n\n"
EXTRATO_FINAL = f"\n\n{''.center(20, '-')}"

def criar_usuario(cpf):
    nome = input('Insira o seu nome: ')
    data_nascimento = solicitar_data_nascimento()
    if data_nascimento == 'tentativas excedidas':                                               # Retorna None caso o usuário tenha inserido a data de nascimento no formato errado 3 vezes
        return None
    
    print("Insira seu endereço: ")
    logradouro = input('Logradouro: ')
    numero = input('Número: ')
    bairro = input('Bairro: ')
    cidade = input('Cidade: ')
    estado = solicitar_sigla_estado()
    if estado == 'tentativas excedidas':                                                        # Retorna None caso o usuário tenha inserido errado a sigla do estado 3 vezes
        return None
    
    endereco = " - ".join([logradouro + f', {numero}', bairro, cidade]) + f'/{estado}'          # Formatação do endereço
    ativo = True
    novo_usuario = {                                                                            # Novo Usuário criado como um dicionário
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco,
        'ativo': ativo,
    }
    return novo_usuario

# Solicita a data de nascimento e verifica se foi inserida no formato correto
def solicitar_data_nascimento():                                                                  
    tentativas = 0
    global MAX_TENTATIVAS
    
    FORMATO = '%d/%m/%Y'
    while MAX_TENTATIVAS > tentativas:                                                         # Loop onde é solicitada a data e nascimento e verificada sua validade
        data_nascimento = input('Insira sua data de nascimento no formato dd/mm/aaaa: ')
        try:
            bool(datetime.strptime(data_nascimento, FORMATO))                                   # Testa o formato da data
            return data_nascimento
        except ValueError:
            print('Data inválida, por favor insira sua data de nascimento no formato descrito.')
        tentativas += 1
        print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return 'tentativas excedidas'

# Solicita o cpf e verifica se foi inserido no formato correto
def solicitar_cpf():
    tentativas = 0
    global MAX_TENTATIVAS
    while MAX_TENTATIVAS > tentativas:
        cpf = input('Insira seu número de cpf(somente os números): ')
        if len(cpf) == 11:
            try:
                int(cpf)
                return cpf
            except ValueError:
                print('\nCPF inválido. Insira somente os números do seu CPF.')
        else:
            print('\nCPF inválido. O valor inserido deve conter 11 dígitos.')
        tentativas += 1
        print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}\n')
    
    return 'tentativas excedidas'

# Solicita a sigla do estado do usuário e verifica se ela corresponde a uma das siglas dos estados brasileiros
def solicitar_sigla_estado():
    ESTADOS = (
        'RS',
        'SC',
        'PR',
        'SP',
        'MG',
        'RJ',
        'ES',
        'MT',
        'MS',
        'GO',
        'DF',
        'BA',
        'SE',
        'AL',
        'PE',
        'PB',
        'RN',
        'CE',
        'PI',
        'MA',
        'TO',
        'PA',
        'AM',
        'RO',
        'AC',
        'RR',
        'AP',
    )
    tentativas = 0
    global MAX_TENTATIVAS

    while MAX_TENTATIVAS > tentativas:
        estado = input('Sigla do estado: ').upper()
        if estado in ESTADOS:
            return estado
        else: 
            print('\nSigla inválida. Insira a sigla de um dos estados brasileiros.')
        tentativas += 1
        print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}\n')
    
    return 'tentativas excedidas'

# Verifica se o cpf informado já está presente na lista de usuários
def verificar_cpf(cpf):
    for cliente in usuarios:
        if cliente.get('cpf') == cpf:
            return True
    
    return False

# Encontra todas as contas vinculadas a um CPF as retorna em uma lista
def encontrar_contas(cpf):
    lista_contas_usuario = []

    for conta in contas:
        if conta['cpf'] == cpf and conta['ativa']:
            lista_contas_usuario.append(conta)
    
    return lista_contas_usuario

# Cria uma nova conta corrente associada a um usuário já existente
def criar_conta_corrente(cpf):
    agencia = '0001'
    # Optei por, inicialmente, apenas desativar contas sem excluí-las, tentando simular uma situação real de um banco que precisa manter as informações de contas desativadas
    # por alguns anos. No entanto para que essa parte de determinar o número da nova conta não precisasse ser reescrita no futuro com a inclusão de uma funcionalidade de exclusão
    # de contas, optei por determinar o número da nova conta baseado no número da última conta da lista ao invés do tamanho da lista(que diminuiria em caso de exclusão de uma conta,
    # levando a criação de contas com o mesmo número)
    numero_conta = 1 if len(contas) == 0 else contas[-1]['numero_conta'] + 1
    saldo = 0
    extrato = ''
    saques_hoje = 0
    ativa = True
    nova_conta = {
        'agencia': agencia,
        'numero_conta': numero_conta,
        'cpf': cpf,
        'saldo': saldo,
        'extrato': extrato,
        'saques_hoje': saques_hoje,
        'ativa': ativa,
    }
    return nova_conta

def cadastrar_usuario(cpf):
    global MAX_TENTATIVAS
    MENU_CADASTRO_CLIENTE = '''
[1] Cadastrar
[0] Sair
'''
    print("\nVerificamos que o CPF informado não está cadastrado no nosso banco de dados de clientes. Gostaria de se cadastrar?")
    
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print(MENU_CADASTRO_CLIENTE)
        opcao = input('Escolha uma das opções: ')
        if opcao == '1':
            novo_usuario = criar_usuario(cpf)
            # Se alguma das etapas da criação do novo usuário falhar por número máximo de tentativas excedido, o atendimento é terminado
            if novo_usuario == None:    
                tentativas = MAX_TENTATIVAS
                break
            # Se a criação do novo usuário for bem sucedida, o usuário é levado para o menu de contas
            else:
                usuarios.append(novo_usuario)
                print('\nCadastro realizado com sucesso. Obrigado por se tornar nosso cliente!')
                gerenciar_contas(cpf)
                break
        # Se o usuário optar por sair, o atendimento é terminado sem as mensagens de "Tentativas Restantes" ou "Tentativas excedidas" serem exibidas
        elif opcao == '0':
            break
        else:
            tentativas += 1
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')

    if tentativas >= MAX_TENTATIVAS:
        print('Número máximo de tentativas excedido.')

# Transforma um usuário cadastrado em inativo, o que é um requerimento para que seja excluído
def desativar_usuario(cpf):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            usuario['ativo'] = False

def registrar_nova_conta(cpf):
    nova_conta = criar_conta_corrente(cpf)
    contas.append(nova_conta)
    print(f'\nNova conta corrente criada: Agência: {nova_conta['agencia']}, Conta: {nova_conta['numero_conta']}')

def desativar_conta(*, agencia, numero_conta, lista_contas_usuario):
    for conta in lista_contas_usuario:
        if conta['agencia'] == agencia and conta['numero_conta'] == numero_conta:
            # IMPLEMENTAR SAQUE ESPECIAL PARA ZERAR A CONTA DESATIVADA
            conta['ativa'] = False
            return 'conta desativada'
    print('\nAgência ou número da conta não correspondem às contas vinculadas a este usuário.')
    return 'conta nao encontrada'

# Pega uma lista de contas e formata em uma string
def listar_contas(contas_usuario):
    res = ''
    for conta in contas_usuario:
        res += f'Agência: {conta['agencia']}, Conta: {conta['numero_conta']}\n'
    return res


def gerenciar_contas(cpf):
    global MAX_TENTATIVAS
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        contas_usuario = encontrar_contas(cpf)
        contas_formatadas = listar_contas(contas_usuario)
        possui_contas = len(contas_usuario) != 0
        MENU_CONTAS = f'''
[1] Criar nova conta corrente
[2] Movimentar conta corrente {'- INDISPONÍVEL' if not possui_contas else ''}
[3] Desativar conta corrente {'- INDISPONÍVEL' if not possui_contas else ''}
[4] Desativar usuário {'- INDISPONÍVEL' if possui_contas else ''}
[0] Sair

'''
        print(f'\n{'Suas contas:' if len(contas_usuario) > 0 else 'Não há contas corrente registradas neste CPF.'}' + f'\n{contas_formatadas}' + MENU_CONTAS)
        opcao = input('Escolha uma das opções: ')
        # Abrir nova conta corrente
        if opcao == '1':
            registrar_nova_conta(cpf)
            tentativas = 0
            print('\nComo mais podemos ajudá-lo?')
        elif opcao == '2':
            break
        # Desativar Conta Corrente
        elif opcao == '3':
            print('\nInsira os dados da conta que deseja desativar.')
            agencia = input('Agência: ')
            numero_conta = input('Número da conta: ')
            res = desativar_conta(agencia=agencia, numero_conta=numero_conta, lista_contas_usuario=contas_usuario)
            if res == 'conta desativada':
                tentativas = 0
                print('\nComo mais podemos ajudá-lo?')
            elif res == 'conta nao encontrada':
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
        # Desativar Usuário
        elif opcao == '4':
            if not possui_contas:
                desativar_usuario(cpf)
                print('\nLamentamos que esteja de saída.')
                break
            else:
                tentativas += 1
                print('\nNão podemos excluir o usuário atual enquanto houver contas vinculadas ao mesmo.')
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
        # SAIR
        elif opcao == '0':
            break
        # Input não corresponde a nenhuma das opções
        else:
            tentativas += 1
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
        # Input que não corresponde a nenhuma das opções disponíveis inserido 3 vezes seguidas
        if tentativas >= MAX_TENTATIVAS:
            print('Número máximo de tentativas excedido.')

            
    



# Inicio do programa
def iniciar_atendimento():
    MENSAGEM_INICIAL = '''
Bem vindo(a) ao Banco X!
'''
    print(MENSAGEM_INICIAL)
    cpf = solicitar_cpf()
    if cpf == 'tentativas excedidas':
        print('Número máximo de tentativas excedido.')
    else:
        if verificar_cpf(cpf):
            gerenciar_contas(cpf)
        else:
            cadastrar_usuario(cpf)
    
    print('\nObrigado por utilizar os nossos serviços!\n')

        
iniciar_atendimento()
print(usuarios)


# while True:
#     acao = input(MENU)

#     # Depósito
#     if acao == '1':
#         valor = float(input('Informe o valor do seu depósito: R$ '))
#         # Depósito negativo ou igual a 0
#         if valor <= 0:
#             print('\nSó são aceitos depósitos de valores positivos.')
#         # Depósito válido
#         else:
#             saldo += valor
#             extrato += f'Depósito: + R$ {valor:.2f}\n'
#             print(f'\nDepósito no valor de R$ {valor:.2f} realizado com sucesso.')
    
#     # Saque
#     elif acao == '2':

#         # Limite de saques diários não atingido
#         if saques_realizados_hoje < LIMITE_SAQUES_DIARIOS:
#             # global saldo, saques_realizados_hoje, extrato
#             valor = float(input('Informe o valor que deseja sacar: R$ '))
#             # Saque negativo ou igual a 0
#             if valor <= 0:
#                 print('\nSó são aceitos saques de valores positivos.')
#             # Saque maior que o limite
#             elif valor > LIMITE_SAQUE:
#                 print(f"\nSó são permitidos saques de até R$ {LIMITE_SAQUE:.2f}.")
#             # Saque maior que o saldo
#             elif valor > saldo:
#                 print('\nSaldo Insuficiente. Não foi possível realizar a transação.')
#             # Saque válido
#             else:
#                 saldo -= valor
#                 extrato += f"Saque: - R$ {valor:.2f}\n"
#                 saques_realizados_hoje += 1
#                 print(f'\nSaque no valor de R$ {valor:.2f} realizado com sucesso. Retire o seu dinheiro.')
    
#         # Limite de saques diários atingido
#         else:
#             print('\nO limite de 3 saques diários já foi atingido.')
    
#     # Extrato
#     elif acao == '3':
#         # Extrato vazio
#         if extrato == f"{' EXTRATO '.center(20, '-')}\n\n":
#             print(extrato + 'Não foram realizadas movimentações.')
#         # Extrato com movimentações
#         else:
#             print(extrato + f"\nSaldo atual: R$ {saldo:.2f}")

#     # Fim da operação
#     elif acao == '0':
#         print('\nObrigado por utilizar os nossos serviços!')
#         break

#     else:
#         print('Opção inválida. Selecione uma das opções apresentadas.')
#         continue
    
#     print('\nPodemos lhe ajudar com algo mais?')