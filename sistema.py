from datetime import datetime

MENSAGEM_INICIAL = '''
Bem vindo(a) ao Banco X!
'''
MENU = f'''
{' MENU '.center(20, '-')}

[1] Depósito
[2] Saque
[3] Extrato
[0] Sair

'''
usuarios = []
contas = []
saldo = 0
saques_realizados_hoje = 0
LIMITE_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3
EXTRATO_INICIO = f"{' EXTRATO '.center(20, '-')}\n\n"
EXTRATO_FINAL = f"\n\n{''.center(20, '-')}"

def criar_usuario():
    nome = input('Insira o seu nome: ')
    data_nascimento = solicitar_data_nascimento()
    if data_nascimento == 'tentativas excedidas':                                               # Retorna None caso o usuário tenha inserido a data de nascimento no formato errado 3 vezes
        return None
    
    cpf = solicitar_cpf()
    if cpf == 'tentativas excedidas':                                                           # Retorna None caso o usuário tenha inserido o cpf no formato errado 3 vezes
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
    novo_usuario = {                                                                            # Novo Usuário criado como um dicionário
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    return novo_usuario

# Solicita a data de nascimento e verifica se foi inserida no formato correto
def solicitar_data_nascimento():                                                                  
    tentativas = 0
    MAX_TENTATIVAS = 3
    
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
    MAX_TENTATIVAS = 3
    while MAX_TENTATIVAS > tentativas:
        cpf = input('Insira seu número de cpf(somente os números): ')
        if len(cpf) == 11:
            try:
                int(cpf)
                return cpf
            except ValueError:
                print('CPF inválido. Insira somente os números do seu CPF.')
        else:
            print('CPF inválido. O valor inserido deve conter 11 dígitos.')
        tentativas += 1
        print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    
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
    MAX_TENTATIVAS = 3

    while MAX_TENTATIVAS > tentativas:
        estado = input('Sigla do estado: ').upper()
        if estado in ESTADOS:
            return estado
        else: 
            print('Sigla inválida. Insira a sigla de um dos estados brasileiros.')
        tentativas += 1
        print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    
    return 'tentativas excedidas'

# Verifica se o cpf informado já está presente na lista de usuários
def verificar_cpf(lista_clientes, *, cpf):
    
    for cliente in lista_clientes:
        if cliente.get('cpf') == cpf:
            return True
    
    return False

# Cria uma nova conta corrente associada a um usuário já existente
def criar_conta_corrente(contas, *, cpf):
    agencia = '0001'
    numero_conta = len(contas) + 1
    saldo = 0
    extrato = ''
    saques_hoje = 0
    nova_conta = {
        'agencia': agencia,
        'numero_conta': numero_conta,
        'cpf': cpf,
        'saldo': saldo,
        'extrato': extrato,
        'saques_hoje': saques_hoje,
    }
    return nova_conta

print(MENSAGEM_INICIAL)

# cpf = solicitar_cpf()
# if cpf == 'tentativas excedidas':
#     print('Número máximo de tentativas excedido. Encerrando a sessão.')
# else:

    


while True:
    acao = input(MENU)

    # Depósito
    if acao == '1':
        valor = float(input('Informe o valor do seu depósito: R$ '))
        # Depósito negativo ou igual a 0
        if valor <= 0:
            print('\nSó são aceitos depósitos de valores positivos.')
        # Depósito válido
        else:
            saldo += valor
            extrato += f'Depósito: + R$ {valor:.2f}\n'
            print(f'\nDepósito no valor de R$ {valor:.2f} realizado com sucesso.')
    
    # Saque
    elif acao == '2':

        # Limite de saques diários não atingido
        if saques_realizados_hoje < LIMITE_SAQUES_DIARIOS:
            # global saldo, saques_realizados_hoje, extrato
            valor = float(input('Informe o valor que deseja sacar: R$ '))
            # Saque negativo ou igual a 0
            if valor <= 0:
                print('\nSó são aceitos saques de valores positivos.')
            # Saque maior que o limite
            elif valor > LIMITE_SAQUE:
                print(f"\nSó são permitidos saques de até R$ {LIMITE_SAQUE:.2f}.")
            # Saque maior que o saldo
            elif valor > saldo:
                print('\nSaldo Insuficiente. Não foi possível realizar a transação.')
            # Saque válido
            else:
                saldo -= valor
                extrato += f"Saque: - R$ {valor:.2f}\n"
                saques_realizados_hoje += 1
                print(f'\nSaque no valor de R$ {valor:.2f} realizado com sucesso. Retire o seu dinheiro.')
    
        # Limite de saques diários atingido
        else:
            print('\nO limite de 3 saques diários já foi atingido.')
    
    # Extrato
    elif acao == '3':
        # Extrato vazio
        if extrato == f"{' EXTRATO '.center(20, '-')}\n\n":
            print(extrato + 'Não foram realizadas movimentações.')
        # Extrato com movimentações
        else:
            print(extrato + f"\nSaldo atual: R$ {saldo:.2f}")

    # Fim da operação
    elif acao == '0':
        print('\nObrigado por utilizar os nossos serviços!')
        break

    else:
        print('Opção inválida. Selecione uma das opções apresentadas.')
        continue
    
    print('\nPodemos lhe ajudar com algo mais?')