from datetime import datetime
from classes import Conta, ContaCorrente, Deposito, Saque, Historico, Cliente, PessoaFisica

MENU = f'''
{' MENU '.center(20, '-')}

[1] Depósito
[2] Saque
[3] Extrato
[0] Sair

'''
usuarios = [
    {'nome': 'Teste', 'data_nascimento': '01/01/1900', 'cpf': '00000000000', 'endereco': 'Rua Teste, 0 - Bairro - Cidade/ES', 'ativo': True},
    {'nome': 'Teste A', 'data_nascimento': '01/01/2001', 'cpf': '11111111111', 'endereco': 'Rua A, 1 - Bairro A - Cidade A/AM', 'ativo': True},
    {'nome': 'Teste B', 'data_nascimento': '02/02/2002', 'cpf': '22222222222', 'endereco': 'Rua B, 2 - Bairro B - Cidade B/BA', 'ativo': False},
    {'nome': 'Teste C', 'data_nascimento': '03/03/2003', 'cpf': '33333333333', 'endereco': 'Rua C, 3 - BAirro C - Cidade C/CE', 'ativo': False},
    {'nome': 'Teste D', 'data_nascimento': '04/04/2004', 'cpf': '44444444444', 'endereco': 'Rua D, 4 - Bairro D - Cidade D/PE', 'ativo': False},
    {'nome': 'TESTE E', 'data_nascimento': '05/05/2005', 'cpf': '55555555555', 'endereco': 'RUA E, 5 - Bairro E - CIdade E/ES', 'ativo': False}
]
contas = [
    {'agencia': '0001', 'numero_conta': 1, 'cpf': '00000000000', 'saldo': 480.0, 'extrato': 'Depósito: R$ 500.00\nSaque: R$ 20.00\n', 'saques_hoje': 1, 'ativa': True},
    {'agencia': '0001', 'numero_conta': 2, 'cpf': '00000000000', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 3, 'cpf': '00000000000', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 4, 'cpf': '00000000000', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 5, 'cpf': '11111111111', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 6, 'cpf': '11111111111', 'saldo': 90.0, 'extrato': 'Depósito: R$ 200.00\nSaque: R$ 30.00\nSaque: R$ 70.00\nSaque: R$ 10.00\n', 'saques_hoje': 3, 'ativa': True},
    {'agencia': '0001', 'numero_conta': 7, 'cpf': '11111111111', 'saldo': 0.0, 'extrato': 'Depósito: R$ 1000.00\nSaque: R$ 320.00\nSaque final: R$ 680.00\n', 'saques_hoje': 1, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 8, 'cpf': '11111111111', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 9, 'cpf': '22222222222', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 10, 'cpf': '22222222222', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 11, 'cpf': '22222222222', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 12, 'cpf': '33333333333', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 13, 'cpf': '33333333333', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 14, 'cpf': '33333333333', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False},
    {'agencia': '0001', 'numero_conta': 15, 'cpf': '33333333333', 'saldo': 0.0, 'extrato': '', 'saques_hoje': 0, 'ativa': False}
]
MAX_TENTATIVAS = 3
LIMITE_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3

# Formata e imprime o extrato
def exibir_extrato(saldo, /, *, extrato):
    print(f"{' EXTRATO '.center(30, '=')}\n")
    print(f'{extrato}')
    print(f'Saldo: R$ {saldo:.2f}\n')
    print(''.center(30, '='))

def novo_exibir_extrato(saldo: float, /, *, agencia: str, numero: int, titular: str, historico: Historico):
    print(f'Agencia: {agencia}')
    print(f'Número da conta: {numero}')
    print(f'Titular: {titular}')
    print(f"{' EXTRATO '.center(60, '=')}\n")
    for entrada in historico.transacoes:
        print(f'{entrada['data'].strftime('%d-%m-%Y %H:%M:%S')} {entrada['tipo']}: R$ {entrada['valor']:.2f}')
    print()
    print(f'Saldo: R$ {saldo:.2f}\n')
    print(''.center(60, '='))

# Função de depósito
def depositar(conta, /):
    global MAX_TENTATIVAS
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        # bloco para receber o input do usuário, atendendo aos requerimentos de um depósito, onde o valor inserido deve ser numérico e maior que 0
        try:
            valor = float(input('Insira o valor a ser depositado: '))
            if valor <= 0:
                # desvia a execução para o except para tratar o caso de um input não permitido
                raise ValueError('Depósito menor ou igual a 0')
            conta['saldo'] += round(valor, 2)
            conta['extrato'] += f'Depósito: R$ {valor:.2f}\n'
            print(f'\nDepósito no valor de R$ {valor:.2f} efetuado com sucesso.')
            return 'deposito efetuado'
        except ValueError:
            tentativas += 1
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            print('\nInsira um valor numérico maior que 0.')
    return 'tentativas excedidas'

# Função de saque
def sacar(*, conta):
    global MAX_TENTATIVAS, LIMITE_SAQUE
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        # bloco para receber o input do usuário, atendendo aos requerimentos de um saque, onde o valor inserido deve ser numérico, maior que 0 e menor que o saldo da conta
        try:
            valor = float(input('Insira o valor a ser sacado: '))
            # desvia a execução para o except para tratar o caso de um input não permitido
            if valor <= 0:
                raise ValueError('Menor que 0')
            elif valor > conta['saldo']:
                raise ValueError('Valor maior que o saldo')
            elif valor > LIMITE_SAQUE:
                raise ValueError('Valor maior que o limite')
            conta['saldo'] -= round(valor, 2)
            conta['extrato'] += f'Saque: R$ {valor:.2f}\n'
            conta['saques_hoje'] += 1
            print(f'\nSaque no valor de R$ {valor:.2f} efetuado com sucesso.')
            return 'saque efetuado'
        except ValueError as err:
            tentativas += 1
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            # Exibe ao usuário mensagens diferentes de acordo com o tipo de erro ocorrido
            if err.args[0] == 'Valor maior que o saldo':
                print('\nSaldo Insuficiente.')
            elif err.args[0] == 'Valor maior que o limite':
                print(f'\nO valor limite para saques é de R$ {LIMITE_SAQUE:.2f}.')
            else:
                print('\nInsira um valor numérico maior que 0.')
    return 'tentativas excedidas'

# Efetua um saque igual a todo o valor do saldo. Exclusivo para contas que estão sendo desativadas
def saque_final(*, conta):
    valor = conta['saldo']
    conta['saldo'] = 0.0
    conta['extrato'] += f'Saque final: R$ {valor:.2f}\n'
    print(f'\nSaque final no valor de R$ {valor:.2f} efetuado com sucesso.')

# Lida com a criação de um novo usuário que será posteriormente adicionado a lista de usuários do banco
def criar_usuario(cpf):
    nome = input('Insira o seu nome: ')
    data_nascimento = solicitar_data_nascimento()
    # Retorna None caso o usuário tenha inserido a data de nascimento no formato errado 3 vezes
    if data_nascimento == 'tentativas excedidas':
        return None
    
    print("Insira seu endereço: ")
    logradouro = input('Logradouro: ')
    numero = input('Número: ')
    bairro = input('Bairro: ')
    cidade = input('Cidade: ')
    estado = solicitar_sigla_estado()
    # Retorna None caso o usuário tenha inserido errado a sigla do estado 3 vezes
    if estado == 'tentativas excedidas':                                                        
        return None
    # Formatação do endereço
    endereco = " - ".join([logradouro + f', {numero}', bairro, cidade]) + f'/{estado}'          
    ativo = True
    # Novo Usuário criado como um dicionário
    novo_usuario = {                                                                            
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco,
        'ativo': ativo,
    }
    return novo_usuario

# Solicita o cpf e verifica se foi inserido no formato correto
def solicitar_cpf():
    tentativas = 0
    global MAX_TENTATIVAS
    while MAX_TENTATIVAS > tentativas:
        cpf = input('Insira seu número de cpf(somente os números) ou digite "sair" para encerra a sessão: ')
        # Acesso ao menu de gerenciamento do banco, que permite exclusão permanente de usuários e contas corrente desativados, bem como a reinicialização dos saques diários
        # de contas individuais ou de todas
        if cpf == 'adm':
            return 'adm'
        # Input para encerra a execução do programa
        elif cpf == 'sair':
            return 'sair'
        elif len(cpf) == 11:
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

# Verifica se o cpf informado já está presente na lista de usuários
def verificar_cpf(cpf):
    for cliente in usuarios:
        if cliente.get('cpf') == cpf:
            return True
    
    return False

# Solicita a data de nascimento e verifica se foi inserida no formato correto
def solicitar_data_nascimento():                                                                  
    tentativas = 0
    global MAX_TENTATIVAS
    
    FORMATO = '%d/%m/%Y'
    # Loop onde é solicitada a data e nascimento e verificada sua validade
    while MAX_TENTATIVAS > tentativas:                                                        
        data_nascimento = input('Insira sua data de nascimento no formato dd/mm/aaaa: ')
        # Testa o formato da data
        try:
            bool(datetime.strptime(data_nascimento, FORMATO))                                   
            return data_nascimento
        except ValueError:
            print('Data inválida, por favor insira sua data de nascimento no formato descrito.')
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

# Transforma um usuário cadastrado em inativo, o que é um requerimento para que seja excluído
def desativar_usuario(cpf):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            usuario['ativo'] = False

# Verifica se há usuarios desativados
def verificar_usuarios_desativados():
    for usuario in usuarios:
        if not usuario['ativo']:
            return True
    return False

# Exclui um usuário desativado
def excluir_usuario(cpf):
    user_index = 'usuario nao encontrado'
    # Percorre a lista de usuários
    for index, usuario in enumerate(usuarios):
        # Quando uma correspondencia com o CPF passado é encontrada
        if usuario['cpf'] == cpf:
            # Checa se o usuário está realmente inativo
            if usuario['ativo']:
                return 'usuario ativo'
            # Salva o índice do usuário
            else:
                user_index = index
                break
    # Se nenhum usuário com o cpf passado é encontrado retorna uma mensagem descritiva
    if user_index == 'usuario nao encontrado':
        return 'usuario nao encontrado'
    # Exclui todas as contas corrente do usuário e então exclui o usuário
    else: 
        excluir_todas_contas_de_um_usuario(cpf)
        del usuarios[user_index]
        return 'usuario excluido'
                
def excluir_todos_usuarios_desativados():
    # Percorre a lista de usuários ao contrário para evitar que a exclusão de um usuário afete o índice de outro a ser excluído
    for i in range(len(usuarios) - 1, -1, -1):
        # Checa se o usuário está inativo
        if not usuarios[i]['ativo']:
            # Exclui todas as contas vinculadas ao usuário
            excluir_todas_contas_de_um_usuario(usuarios[i]['cpf'])
            # Exclui o usuário
            del usuarios[i]

# Cria uma nova conta corrente associada a um usuário já existente
def criar_conta_corrente(cpf):
    agencia = '0001'
    # Optei por determinar o número da nova conta baseado no número da última conta da lista ao invés do tamanho da lista(que diminuiria em caso de exclusão de uma conta,
    # levando a criação de contas com o mesmo número)
    numero_conta = 1 if len(contas) == 0 else contas[-1]['numero_conta'] + 1
    saldo = 0.0
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

# Lida com o registro de novas contas corrente
def registrar_nova_conta(cpf):
    nova_conta = criar_conta_corrente(cpf)
    contas.append(nova_conta)
    print(f'\nNova conta corrente criada: Agência: {nova_conta['agencia']}, Conta: {nova_conta['numero_conta']}')

# Lida com a desativação de contas, que é zerada caso ainda possua saldo
def desativar_conta(*, agencia, numero_conta, lista_contas_usuario):
    for conta in lista_contas_usuario:
        if conta['agencia'] == agencia and str(conta['numero_conta']) == numero_conta:
            if conta['saldo'] > 0:
                saque_final(conta=conta)
            conta['ativa'] = False
            return 'conta desativada'
    print('\nAgência ou número da conta não correspondem às contas vinculadas a este usuário.')
    return 'conta nao encontrada'

# Encontra todas as contas vinculadas a um CPF as retorna em uma lista
def encontrar_contas(cpf):
    lista_contas_usuario = []

    for conta in contas:
        if conta['cpf'] == cpf and conta['ativa']:
            lista_contas_usuario.append(conta)
    
    return lista_contas_usuario

# Encontra e retorna uma conta de acordo com o numero da agencia e o numero da conta
def encontrar_uma_conta(*, agencia, numero_conta):
    for conta in contas:
        if conta['agencia'] == agencia and str(conta['numero_conta']) == numero_conta:
            return conta
    return 'conta nao encontrada'

# Pega uma lista de contas e formata em uma string
def listar_contas(contas_usuario):
    res = ''
    for conta in contas_usuario:
        res += f'Agência: {conta['agencia']}, Conta: {conta['numero_conta']}\n'
    return res

# Reseta o contador de saques diário de todas as contas
def resetar_saques_diarios_todos():
    for conta in contas:
        conta['saques_hoje'] = 0
    print('\nContador de saques diário de todas as contas resetado.')

# Reseta o contador de saques diário de uma única conta caso ela exista e retorna o resultado da busca
def resetar_saques_diarios_uma_conta(*, agencia, numero_conta):
    conta_encontrada = False
    for conta in contas:
        if conta['agencia'] == agencia and str(conta['numero_conta']) == numero_conta:
            conta['saques_hoje'] = 0
            conta_encontrada = True
    return conta_encontrada

# Exclui uma conta desativada
def excluir_conta(*, agencia, numero_conta):
    for i, conta in enumerate(contas):
        if conta['agencia'] == agencia and str(conta['numero_conta']) == numero_conta:
            if conta['ativa']:
                return 'conta ativa'
            else:
                del contas[i]
                return 'conta deletada'
    return 'conta nao encontrada'

# Exclui todas as contas de um usuário
def excluir_todas_contas_de_um_usuario(cpf):
    # Percorre a lista de contas ao contrário para que a exclusão de uma conta não afete o índice da próxima conta a ser excluída
    for i in range(len(contas) - 1, -1, -1):
        if contas[i]['cpf'] == cpf:
            del contas[i]
    print(f'\nTodas as contas do usuário de CPF {cpf} foram excluídas.')

def excluir_todas_contas_desativadas_de_um_usuario(cpf):
    # Percorre a lista de contas ao contrário para que a exclusão de uma conta não afete o índice da próxima conta a ser excluída
    for i in range(len(contas) - 1, -1, -1):
        if contas[i]['cpf'] == cpf and not contas[i]['ativa']:
            del contas[i]
    print(f'\nTodas as contas desativadas do usuário de CPF {cpf} foram excluídas.')

# Exclui todas as contas desativadas
def excluir_todas_contas_desativadas():
    # Percorre a lista de contas ao contrário para que a exclusão de uma conta não afete o índice da próxima conta a ser excluída
    for i in range(len(contas) - 1, -1, -1):
        if not contas[i]['ativa']:
            del contas[i]

# Verifica se há contas desativadas
def verificar_contas_desativadas():
    for conta in contas:
        if not conta['ativa']:
            return True
    return False

# Lida com o registro de novos usuários
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

# Função responsável pelas opções do menu de movimentação de contas, ou seja, saques, depósitos e impressão de extratos
def movimentar_contas(*, agencia, numero_conta, lista_contas_usuario):
    global MAX_TENTATIVAS, LIMITE_SAQUES_DIARIOS
    conta_escolhida = {}
    # Encontra a conta selecionada
    for conta in lista_contas_usuario:
        if conta['agencia'] == agencia and str(conta['numero_conta']) == numero_conta:
            conta_escolhida = conta
    # Se nenhuma conta com os parâmetros passados for encontrada, retorna a função
    if len(conta_escolhida) == 0:
        print('\nAgência ou número da conta não correspondem às contas vinculadas a este usuário.')
        return 'conta nao encontrada'
    else:
        tentativas = 0
        while tentativas < MAX_TENTATIVAS:
            MENU_OPERACOES = f'''
Agencia: {conta_escolhida['agencia']} Conta: {conta_escolhida['numero_conta']}
Saldo: R$ {conta_escolhida['saldo']:.2f}

[1] Saque {'- INDISPONÍVEL' if conta_escolhida['saldo'] <= 0 or conta_escolhida['saques_hoje'] >= LIMITE_SAQUES_DIARIOS else ''}
[2] Depósito
[3] Extrato
[0] Sair
'''
            print(MENU_OPERACOES)
            opcao = input('Escolha uma das opções: ')
            # Efetuar saque
            if opcao == '1':
                # Não permite mais de 3 saques por dia
                if conta_escolhida['saques_hoje'] >= LIMITE_SAQUES_DIARIOS:
                    print('\nLimite de 3 saques diários atingido, operação não efetuada.')
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                # Não permite efetuar saques em contas sem saldo
                elif conta_escolhida['saldo'] <= 0:
                    print('\nSaldo insuficiente.')
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                else:
                    res = sacar(conta=conta_escolhida)
                    if res == 'tentativas excedidas':
                        return 'tentativas excedidas'
                    elif res == 'saque efetuado':
                        tentativas = 0

            # Efetuar depósito
            elif opcao == '2':
                res = depositar(conta_escolhida)
                if res == 'tentativas excedidas':
                    return 'tentativas excedidas'
                elif res == 'deposito efetuado':
                    tentativas = 0
            # Imprimir extrato
            elif opcao == '3':
                exibir_extrato(conta_escolhida['saldo'], extrato=conta_escolhida['extrato'])
                tentativas = 0
            # SAIR
            elif opcao == '0':
                break
            else:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            # Input que não corresponde a nenhuma das opções disponíveis inserido 3 vezes seguidas
            if tentativas >= MAX_TENTATIVAS:
                return 'tentativas excedidas'
                    
        return 'operacao bem sucedida'

# Função responsável pelas opções do menu de gerenciamento de contas, ou seja, criação, movimentação e desativação de contas corrente e desativação de usuário
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
        # Movimentar conta corrente
        elif opcao == '2':
            print('\nInsira os dados da conta que deseja movimentar.')
            agencia = input('Agência: ')
            numero_conta = input('Número da conta: ')
            res = movimentar_contas(agencia=agencia, numero_conta=numero_conta, lista_contas_usuario=contas_usuario)
            if res == 'conta nao encontrada':
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            elif res == 'operacao bem sucedida':
                tentativas = 0
                print('\nComo mais podemos ajudá-lo?')
            elif res == 'tentativas excedidas':
                tentativas = 3
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

# Função que permite o gerenciamento de usuários e contas por parte do banco
def gerenciamento_institucional():
    LIMITE_MINIMO_SAQUE = 100.0
    LIMITE_MINIMO_SAQUES_DIARIOS = 1
    global MAX_TENTATIVAS, LIMITE_SAQUE, LIMITE_SAQUES_DIARIOS
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        ha_contas_desativadas = verificar_contas_desativadas()
        ha_usuarios_desativados = verificar_usuarios_desativados()
        print('\n USUARIOS:')
        for usuario in usuarios:
            print(usuario)
        print('\n CONTAS:')
        for conta in contas:
            print(conta)
        MENU_GERENCIAMENTO = f'''
[1] Reinicializar contador de saques diário de todas as contas
[2] Reinicializar contador de saques diário de uma única conta
[3] Excluir usuário desativado {'- INDISPONÍVEL' if not ha_usuarios_desativados else ''}
[4] Excluir todos os usuários desativados {'- INDISPONÍVEL' if not ha_usuarios_desativados else ''}
[5] Excluir todas as contas desativadas de um usuário {'- INDISPONÍVEL' if not ha_contas_desativadas else ''}
[6] Excluir conta desativada {'- INDISPONÍVEL' if not ha_contas_desativadas else ''}
[7] Excluir todas as contas desativadas {'- INDISPONÍVEL' if not ha_contas_desativadas else ''}
[8] Alterar valor limite de saque
[9] Alterar limite de saques diários
[10] Exibir extrato de uma conta {'' if len(contas) > 0 else '- INDISPONÍVEL'}
[0] Sair
'''
        print(MENU_GERENCIAMENTO)
        opcao = input('Escolha uma das opções: ')
        # Reinicializar contador de saques diário de todas as contas
        if opcao == '1':
            resetar_saques_diarios_todos()
            tentativas = 0
        # Reinicializar contador de saques diário de uma única conta
        elif opcao == '2':
            print('\nInsira as informações da conta:')
            agencia = input('Agência: ')
            numero_conta = input('Número da conta: ')
            conta_encontrada = resetar_saques_diarios_uma_conta(agencia=agencia, numero_conta=numero_conta)
            if conta_encontrada:
                tentativas = 0
                print(f'\nO contador de saques diário da conta {numero_conta}, Agencia {agencia} foi resetado.')
            else:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                print(f'\nConta não encontrada.')
        # Excluir usuário desativado
        elif opcao == '3':
            if ha_usuarios_desativados:
                cpf = input('Insira o cpf do usuário a ser excluído: ')
                res = excluir_usuario(cpf)
                if res == 'usuario excluido':
                    tentativas = 0
                    print(f'\nUsuário de CPF {cpf} excluído com sucesso.')
                elif res == 'usuario ativo':
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                    print(f'\nUsuário ativo. Usuários ativos não podem ser excluídos.')
                elif res == 'usuario nao encontrado':
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                    print(f'\nNenhum usuário encontrado com o CPF passado.')
            else:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                print('Opção indisponível. Nenhum usuário desativado foi encontrado.')
        # Excluir todos os usuários desativados
        elif opcao == '4':
            if ha_usuarios_desativados:
                tentativas = 0
                excluir_todos_usuarios_desativados()
                print('\nTodos os usuários desativados e suas respectivas contas foram excluídos com sucesso.')
            else:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                print('Opção indisponível. Nenhum usuário desativado foi encontrado.')
        # Excluir todas as contas desativadas de um usuário
        elif opcao == '5':
            if ha_contas_desativadas:
                cpf = input('Insira o cpf do usuário cujas contas desativadas devem ser excluídas: ')
                if verificar_cpf(cpf):
                    tentativas = 0
                    excluir_todas_contas_desativadas_de_um_usuario(cpf)
                else:
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                    print('Nenhum usuário com o CPF passado foi encontrado.')
            else:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                print('Opção indisponível. Nenhuma conta desativada foi encontrada.')
        # Excluir conta desativada
        elif opcao == '6':
            if ha_contas_desativadas:
                print('\nInsira as informações da conta:')
                agencia = input('Agência: ')
                numero_conta = input('Número da conta: ')
                res = excluir_conta(agencia=agencia, numero_conta=numero_conta)
                if res == 'conta nao encontrada':
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                    print(f'\nConta não encontrada.')
                elif res == 'conta ativa':
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                    print(f'\nConta ativa. Contas ativas não podem ser excluídas.')
                elif res == 'conta deletada':
                    tentativas = 0
                    print(f'\nConta {numero_conta}, Agencia {agencia} foi excluída com sucesso.')
            else:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                print('Opção indisponível. Nenhuma conta desativada foi encontrada.')
        # Excluir todas as contas desativadas
        elif opcao == '7':
            if ha_contas_desativadas:
                tentativas = 0
                excluir_todas_contas_desativadas()
                print('\nTodas as contas desativadas foram excluídas com sucesso.')
            else:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                print('Opção indisponível. Nenhuma conta desativada foi encontrada.')
        # Alterar valor limite de saque
        elif opcao == '8':
            try:
                valor = float(input('Insira o novo valor limite de saque: '))
                # Não é permitido reduzir o valor limite de saque para menos de R$ 100.00
                if valor < LIMITE_MINIMO_SAQUE:
                    raise ValueError('novo valor muito baixo')
                LIMITE_SAQUE = round(valor, 2)
                print(f'\nValor limite de saque atualizado para R$ {valor:.2f}')
                tentativas = 0
            except ValueError as err:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                if err.args[0] == 'novo valor muito baixo':
                    print(f'Não é permitido diminuir o valor limite de saque para menos de R$ {LIMITE_MINIMO_SAQUE:.2f}.')
                else:
                    print(f'Insira um valor numérico positivo e maior ou igual a {LIMITE_MINIMO_SAQUE:.2f}.')
        # Alterar limite de saques diários
        elif opcao == '9':
            try:
                valor = int(input('Insira o novo valor limite de saque: '))
                # Não é permitido reduzir o limite de saques diários para menos de 1
                if valor < LIMITE_MINIMO_SAQUES_DIARIOS:
                    raise ValueError('novo valor muito baixo')
                LIMITE_SAQUES_DIARIOS = valor
                print(f'\nValor limite de saques diários atualizado para: {valor}')
                tentativas = 0
            except ValueError as err:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                if err.args[0] == 'novo valor muito baixo':
                    print(f'Não é permitido diminuir o limite de saques diários para menos de {LIMITE_MINIMO_SAQUES_DIARIOS}.')
                else:
                    print('Insira um valor numérico inteiro positivo.')
        # Exibir o extrato de uma conta
        elif opcao == '10':
            if len(contas) > 0:
                print('\nInsira as informações da conta:')
                agencia = input('Agência: ')
                numero_conta = input('Número da conta: ')
                res = encontrar_uma_conta(agencia=agencia, numero_conta=numero_conta)
                if res == 'conta nao encontrada':
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                    print('\nConta não encontrada.')
                else:
                    tentativas = 0
                    exibir_extrato(res['saldo'], extrato = res['extrato'])
            else:
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                print('Opção Indisponível. Nenhuma conta encontrada.')
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
    while True:
        print(MENSAGEM_INICIAL)
        cpf = solicitar_cpf()
        # Acesso ao menu de gerenciamento do banco, que permite exclusão permanente de usuários e contas corrente desativados, bem como a reinicialização dos saques diários
        # de contas individuais ou de todas
        if cpf == 'adm':
            gerenciamento_institucional()
        # Input para terminar a execução
        elif cpf == 'sair':
            break
        elif cpf == 'tentativas excedidas':
            print('Número máximo de tentativas excedido.')
            break
        else:
            if verificar_cpf(cpf):
                gerenciar_contas(cpf)
            else:
                cadastrar_usuario(cpf)
    
    print('\nObrigado por utilizar os nossos serviços!\n')
   
# iniciar_atendimento()
class teste:
    def __init__(self) -> None:
        self.transacoes = [{'tipo': 'Saque', 'valor': 99.9, 'data': datetime.now()}, {'tipo': 'Deposito', 'valor': 299.9, 'data': datetime.now()}]

novo_exibir_extrato(100.0, agencia='1', numero=1, titular='tonico', historico=teste())