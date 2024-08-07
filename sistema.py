from pathlib import Path
from datetime import datetime, date
from classes import Conta, ContaCorrente, Deposito, Saque, SaqueFinal, Historico, Cliente, PessoaFisica, PessoaJuridica, ContaIterador, decorador_de_log
import csv

ROOT_PATH = Path(__file__).parent

usuarios = []
contas = []
MAX_TENTATIVAS = 3
LIMITE_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3

def imprimir_contas():
    print('CONTAS'.center(100, '-'))
    if len(contas) == 0:
        print()
    else:
        for conta in ContaIterador(contas, extendido=True):
            print(conta)

def imprimir_clientes():
    print('Clientes'.center(100, '-'))
    if len(usuarios) == 0:
        print()
    else:
        for cliente in usuarios:
            print(cliente)

def exibir_extrato_de_uma_conta() -> bool:
    if len(contas) == 0:
        print('\nNenhuma conta encontrada. Recurso indisponível.')
        return True
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print('\nInsira as informações da conta ou "sair" caso deseje abortar a operação:')
        agencia = input('Agência: ')
        if agencia == 'sair':
            return True
        numero_conta = input('Número da conta: ')
        if numero_conta == 'sair':
            return True
        conta = encontrar_uma_conta(agencia=agencia, numero_conta=numero_conta)
        if conta == 'conta nao encontrada':
            tentativas += 1
            print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
        else:
            res = menu_extrato(conta_escolhida=conta)
            return res
    return False


# Formata e imprime o extrato
def exibir_extrato(saldo: float, /, *, agencia: str, numero: int, titular: str, historico: Historico):
    print(f'\nAgencia: {agencia}')
    print(f'Número da conta: {numero}')
    print(f'Titular: {titular}')
    print(f"{' EXTRATO '.center(60, '=')}\n")
    extrato_vazio = True
    for entrada in historico.gerador_de_relatorio():
        print(f"{entrada.data.strftime('%d/%m/%Y %H:%M')} {entrada.tipo}: R$ {entrada.valor:.2f}")
    else:
        extrato_vazio = False
    if extrato_vazio:
        print('Nenhuma movimentação foi realizada nesta conta.')
    print()
    print(f'Saldo: R$ {saldo:.2f}\n')
    print(''.center(60, '='))

# Formata e imprime os saques
def exibir_saques(saldo: float, /, *, agencia: str, numero: int, titular: str, historico: Historico):
    print(f'\nAgencia: {agencia}')
    print(f'Número da conta: {numero}')
    print(f'Titular: {titular}')
    print(f"{' RELATÓRIO - SAQUES '.center(60, '=')}\n")
    extrato_vazio = True
    for entrada in historico.gerador_de_relatorio('Saque'):
        print(f"{entrada.data.strftime('%d/%m/%Y %H:%M')} {entrada.tipo}: R$ {entrada.valor:.2f}")
    else:
        extrato_vazio = False
    if extrato_vazio:
        print('Nenhum saque foi realizado nesta conta.')
    print()
    print(f'Saldo: R$ {saldo:.2f}\n')
    print(''.center(60, '='))

    # Formata e imprime os depositos
def exibir_depositos(saldo: float, /, *, agencia: str, numero: int, titular: str, historico: Historico):
    print(f'\nAgencia: {agencia}')
    print(f'Número da conta: {numero}')
    print(f'Titular: {titular}')
    print(f"{' RELATÓRIO - DEPOSITOS '.center(60, '=')}\n")
    extrato_vazio = True
    for entrada in historico.gerador_de_relatorio('Depósito'):
        print(f"{entrada.data.strftime('%d/%m/%Y %H:%M')} {entrada.tipo}: R$ {entrada.valor:.2f}")
    else:
        extrato_vazio = False
    if extrato_vazio:
        print('Nenhum depósito foi realizado nesta conta.')
    print()
    print(f'Saldo: R$ {saldo:.2f}\n')
    print(''.center(60, '='))

# Função de depósito
def gerenciar_tentativas_deposito(conta: Conta) -> bool:
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        # bloco para receber o input do usuário, atendendo aos requerimentos de um depósito, onde o valor inserido deve ser numérico e maior que 0
        try:
            valor = float(input('Insira o valor a ser depositado ou 0 para abortar a operação: '))
            if valor == 0:
                return True
            # Recebe True se o valor inserido for maior que 0
            deposito_bem_sucedido = conta.depositar(valor)
            # Cria a transação e faz o registro
            if deposito_bem_sucedido:
                deposito = Deposito(valor)
                deposito.registrar(conta)
                return True
            # Se o valor inserido for menor que 0, lança um ValueError
            else:
                raise ValueError('Deposito falhou')
        except ValueError as err:
            tentativas += 1
            # Como a função depositar da classe Conta já imprime um aviso quando o valor inserido é menor que 0
            # optei por somente imprimir um aviso caso o erro for lançado quando o cliente insere um valor não numérico
            if err.args[0] != 'Deposito falhou':
                print('\nInsira um valor numérico maior que 0.')
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return False

# Função de saque
def gerenciar_tentativas_saque(conta: Conta) -> bool:
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        # bloco para receber o input do usuário, atendendo aos requerimentos de um saque, onde o valor inserido deve ser numérico, maior que 0 e menor que o saldo da conta
        try:
            valor = float(input('Insira o valor a ser sacado ou 0 para abortar a operação: '))
            if valor == 0:
                return True
            saque_bem_sucedido = conta.sacar(valor)
            # Cria a transação e faz o registro
            if saque_bem_sucedido:
                saque = Saque(valor)
                saque.registrar(conta)
                return True
            else:
                raise ValueError('Saque falhou')
        except ValueError as err:
            tentativas += 1
            # Como as funções sacar de Conta e de ContaCorrente imprimem avisos quando os requerimentos numéricos
            # não são atingidos, optei por somente imprimir um aviso quando o erro é lançado pelo cliente tentando
            # inserir um valor não numérico
            if err.args[0] != 'Saque falhou':
                print('\nInsira um valor numérico maior que 0.')
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return False

# Efetua um saque igual a todo o valor do saldo. Exclusivo para contas que estão sendo desativadas
def saque_final(*, conta: Conta) -> None:
    valor = conta.saldo
    conta.saque_final()
    saque = SaqueFinal(valor)
    saque.registrar(conta)

def salvar_usuarios() -> None:
    try:
        with open(ROOT_PATH / 'clientes.csv', 'w', newline='', encoding='utf-8') as arquivo:
            registrador = csv.writer(arquivo)
            registrador.writerow(['tipo', 'id', 'nome', 'endereco', 'data_nascimento', 'ativo'])
            for usuario in usuarios:
                if isinstance(usuario, PessoaFisica):
                    registrador.writerow(['PF', usuario.cpf, usuario.nome, usuario.endereco, usuario.data_nascimento.strftime('%d/%m/%Y'), usuario.ativo])
                elif isinstance(usuario, PessoaJuridica):
                    registrador.writerow(['PJ', usuario.cnpj, usuario.nome, usuario.endereco, None, usuario.ativo])
    except IOError as err:
        print('Não foi possível abrir o arquivo')

def carregar_usuarios() -> None:
    try:
        with open(ROOT_PATH / 'clientes.csv', 'r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            for usuario in leitor:
                if usuario['tipo'] == 'PF':
                    dia = int(usuario['data_nascimento'][:2])
                    mes = int(usuario['data_nascimento'][3:5])
                    ano = int(usuario['data_nascimento'][6:])
                    novo_usuario = PessoaFisica(endereco=usuario['endereco'], cpf=usuario['id'], nome=usuario['nome'], data_nascimento=date(ano, mes, dia))
                    usuarios.append(novo_usuario)
                elif usuario['tipo'] == 'PJ':
                    novo_usuario = PessoaJuridica(endereco=usuario['endereco'], cnpj=usuario['id'], nome=usuario['nome'])             
                    usuarios.append(novo_usuario)
                if usuario['ativo'] == 'False':
                    novo_usuario.desativar_conta_cliente()
    except FileNotFoundError as err:
        print('Arquivo de usuários não encontrado.')

def formatar_historico(historico: Historico) -> str:
    historico_conta = f''
    for transacao in historico.transacoes:
        historico_conta += f'{transacao.data.strftime('%d/%m/%Y %H:%M:%S.%f')},{transacao.tipo},{transacao.valor}|'
    return historico_conta[:-1]

def salvar_contas():
    try:
        with open(ROOT_PATH / 'contas.csv', 'w', newline='', encoding='utf-8') as arquivo:
            registrador = csv.writer(arquivo)
            registrador.writerow(['tipo', 'agencia', 'numero', 'cliente', 'saldo', 'limite_transacoes', 'ativa', 'limite', 'limite_saques', 'historico'])
            for conta in contas:
                historico_conta = formatar_historico(conta.historico)
                if isinstance(conta, ContaCorrente):
                    id_cliente = ''
                    if isinstance(conta.cliente, PessoaFisica):
                        id_cliente = conta.cliente.cpf
                    elif isinstance(conta.cliente, PessoaJuridica):
                        id_cliente = conta.cliente.cnpj
                    registrador.writerow([
                        'CC', 
                        conta.agencia, 
                        conta.numero, 
                        id_cliente, 
                        conta.saldo, 
                        conta.limite_transacoes, 
                        conta.ativa, 
                        conta.limite, 
                        conta.limite_saques, 
                        historico_conta
                    ])
    except IOError as err:
        print('Não foi possível abrir o arquivo')

def carregar_historico(conta: Conta, historico_em_str: str) -> None:
    lista_transacoes = historico_em_str.split('|')
    for transacao in lista_transacoes:
        dados_transacao = transacao.split(',')
        data_transacao = datetime.strptime(dados_transacao[0], '%d/%m/%Y %H:%M:%S.%f')
        tipo_transacao = dados_transacao[1]
        valor_transacao = float(dados_transacao[2])
        operacao = None
        if tipo_transacao == 'Saque':
            operacao = Saque(valor_transacao, data=data_transacao)
        elif tipo_transacao == 'Depósito':
            operacao = Deposito(valor_transacao, data=data_transacao)
        elif tipo_transacao == 'Saque Final':
            operacao = SaqueFinal(valor_transacao, data=data_transacao)
        if operacao != None:
            operacao.registrar(conta)
            

# TODO: Adaptar a função para utilizar a chave "tipo" caso mais tipos de contas sejam adicionados
def carregar_contas():
    try:
        with open(ROOT_PATH / 'contas.csv', 'r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            for conta in leitor:
                cliente = None
                if len(conta['cliente']) == 11:
                    cliente = verificar_cpf(conta['cliente'])
                elif len(conta['cliente']) == 14:
                    cliente = verificar_cnpj(conta['cliente'])
                nova_conta = ContaCorrente(agencia=conta['agencia'], numero=int(conta['numero']), cliente=cliente, saldo=float(conta['saldo']), limite_transacoes=int(conta['limite_transacoes']), limite=float(conta['limite']), limite_saques=int(conta['limite_saques']))
                if conta['ativa'] == 'False':
                    nova_conta.desativar_conta()
                carregar_historico(nova_conta, conta['historico'])
                contas.append(nova_conta)
                cliente.adicionar_conta(nova_conta)
    except FileNotFoundError as err:
        print('Arquivo de contas não encontrado.')


# Lida com a criação de um novo usuário que será posteriormente adicionado a lista de usuários do banco
@decorador_de_log
def criar_usuario_pf(cpf: str) -> PessoaFisica | None:
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
    # Novo Usuário criado como uma instância de PessoaFisica
    novo_usuario = PessoaFisica(endereco=endereco, cpf=cpf, nome=nome, data_nascimento=data_nascimento)
    return novo_usuario

@decorador_de_log
def criar_usuario_pj(cnpj: str) -> PessoaJuridica | None:
    nome = input('Insira o seu nome ou nome fantasia: ')
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
    # Novo Usuário criado como uma instância de PessoaJuridica
    novo_usuario = PessoaJuridica(endereco=endereco, cnpj=cnpj, nome=nome)
    return novo_usuario

# Solicita o cpf e verifica se foi inserido no formato correto
def solicitar_cpf() -> str:
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        cpf = input('Insira seu número de CPF(somente os números) ou digite "sair" para encerra a sessão: ')
        # Input para encerra a execução do programa
        if cpf == 'sair':
            break
        # CPFs contem 11 números
        # TODO: Adicionar posteriormente uma função para verificar a validade do CPF através do calculo dos números verificadores
        elif len(cpf) == 11:
            try:
                # Verifica se foram inseridos somente números
                int(cpf)
                return cpf
            except ValueError:
                print('\nCPF inválido. Insira somente os números do seu CPF.')
        else:
            print('\nCPF inválido. O valor inserido deve conter 11 dígitos.')
        tentativas += 1
        print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}\n')
    
    if tentativas >= MAX_TENTATIVAS:
        print('Número máximo de tentativas excedido.')
    return 'sair'

# Solicita o cnpj e verifica se foi inserido no formato correto
def solicitar_cnpj() -> str:
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        cnpj = input('Insira seu número de CNPJ(somente os números) ou digite "sair" para encerra a sessão: ')
        if cnpj == 'sair':
            break
        # CNPJs contém 14 números
        # TODO: Adicionar posteriormente uma função para verificar a validade do CNPJ através do calculo dos números verificadores
        elif len(cnpj) == 14:
            try:
                # Verifica se foram inseridos somente números
                int(cnpj)
                return cnpj
            except ValueError:
                print('\nCNPJ inválido. Insira somente os números do seu CNPJ.')
        else:
            print('\nCNPJ inválido. O valor inserido deve conter 14 dígitos.')
        tentativas += 1
        print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}\n')
    
    if tentativas >= MAX_TENTATIVAS:
        print('Número máximo de tentativas excedido.')
    return 'sair'

# Verifica se o cpf informado já está presente na lista de usuários
def verificar_cpf(cpf: str) -> Cliente | None:
    for cliente in usuarios:
        if isinstance(cliente, PessoaFisica):
            if cliente.cpf == cpf:
                return cliente
    
    return None

# Verifica se o cpf informado já está presente na lista de usuários e retorna o cliente e seu index na lista
def verificar_cpf_index(cpf: str) -> int | None:
    for index, cliente in enumerate(usuarios):
        if isinstance(cliente, PessoaFisica):
            if cliente.cpf == cpf:
                return index
    
    return None

# Verifica se o cnpj informado já está presente na lista de usuários
def verificar_cnpj(cnpj: str) -> Cliente | None:
    for cliente in usuarios:
        if isinstance(cliente, PessoaJuridica):
            if cliente.cnpj == cnpj:
                return cliente
        
    return None

# Verifica se o cnpj informado já está presente na lista de usuários e retorna o cliente e seu index na lista
def verificar_cnpj_index(cnpj: str) -> int | None:
    for index, cliente in enumerate(usuarios):
        if isinstance(cliente, PessoaJuridica):
            if cliente.cnpj == cnpj:
                return index
        
    return None

# Solicita a data de nascimento e verifica se foi inserida no formato correto
def solicitar_data_nascimento() -> date | str:                                                                  
    tentativas = 0
    FORMATO = '%d/%m/%Y'
    # Loop onde é solicitada a data e nascimento e verificada sua validade
    while MAX_TENTATIVAS > tentativas:                                                        
        data_nascimento = input('Insira sua data de nascimento no formato dd/mm/aaaa: ')
        # Testa o formato da data
        try:
            data_nascimento = datetime.strptime(data_nascimento, FORMATO).date()                                   
            return data_nascimento
        except ValueError:
            print('Data inválida, por favor insira sua data de nascimento no formato descrito.\n')
        tentativas += 1
        print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return 'tentativas excedidas'

# Solicita a sigla do estado do usuário e verifica se ela corresponde a uma das siglas dos estados brasileiros
def solicitar_sigla_estado() -> str:
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

    while MAX_TENTATIVAS > tentativas:
        estado = input('Sigla do estado: ').upper()
        # Verifica se o estado inserido corresponde a sigla de algum dos 26 estados + DF
        if estado in ESTADOS:
            return estado
        else: 
            print('\nSigla inválida. Insira a sigla de um dos estados brasileiros.')
        tentativas += 1
        print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}\n')
    
    return 'tentativas excedidas'

# Reativar usuário inativo
def reativacao_cliente(cliente: Cliente) -> bool:
    print('\nDetectamos a existência de um usuário inativo registrado neste CPF.')
    MENSAGEM_ATIVACAO = '''Gostaria de reativar sua conta de usuário?
    
[1] Sim
[0] Não
'''
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print(MENSAGEM_ATIVACAO)
        opcao = input('Escolha uma das opções: ')
        if opcao == '1':
            cliente.reativar_conta_cliente()
            return True
        elif opcao == '0':
            break
        else:
            tentativas += 1
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    
    if tentativas >= MAX_TENTATIVAS:
            print('Número máximo de tentativas excedido.')
    return False


# Verifica se há usuarios desativados
def verificar_usuarios_desativados() -> bool:
    for usuario in usuarios:
        if not usuario.ativo:
            return True
    return False
                
# Exclui um usuário desativado
def excluir_usuario_desativado() -> bool:
    @decorador_de_log
    def excluir_usuario(index):
        del usuarios[index]
    
    ha_usuarios_desativados = verificar_usuarios_desativados()
    if not ha_usuarios_desativados:
        print('\nNenhum usuário desativado encontrado. Recurso indisponível.')
        return True
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        identificacao = input('\nInsira o CPF ou CNPJ(somente os números) do usuário a ser excluído ou "sair" para abortar a operação: ')
        if identificacao == 'sair':
            return True

        try:
            int(identificacao)
            # Pega on indice do cliente selecionado na lista de usuarios
            if len(identificacao) == 11:
                index = verificar_cpf_index(identificacao)
            elif len(identificacao) == 14:
                index = verificar_cnpj_index(identificacao)
            else:
                raise ValueError('\nInsira um número que contenha 11 dígitos(CPF) ou 14 dígitos(CNPJ).')
            
            if index == None:
                raise ValueError('\nCliente não encontrado.')
            elif usuarios[index].ativo:
                raise ValueError('\nClientes ativos não podem ser excluídos.')
            else:
                excluir_todas_contas_desativadas_de_um_usuario(usuarios[index])
                excluir_usuario(index)
                print('\nUsuário excluído com sucesso.')
                return True
        except ValueError as err:
            tentativas += 1
            if err.args[0] == f"invalid literal for int() with base 10: '{identificacao}'":
                print('\nInsira somente os números do CPF ou do CNPJ do usuário a ser excluído.')
            else:
                print(err.args[0])
            print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return False

# Exclui todos os usuários desativados e suas respectivas contas. Sempre retorna True
@decorador_de_log
def excluir_todos_usuarios_desativados() -> bool:
    ha_usuarios_desativados = verificar_usuarios_desativados()
    if not ha_usuarios_desativados:
        print('\nNenhum usuário desativado encontrado. Recurso indisponível.')
        return True
    else:
        # Percorre a lista de usuários ao contrário para evitar que a exclusão de um usuário afete o índice de outro a ser excluído
        for i in range(len(usuarios) - 1, -1, -1):
            # Checa se o usuário está inativo
            if not usuarios[i].ativo:
                # Exclui todas as contas vinculadas ao usuário
                excluir_todas_contas_desativadas_de_um_usuario(usuarios[i])
                # Exclui o usuário
                del usuarios[i]
    print('\nTodos os usuários desativados e suas respectivas contas foram excluídos com sucesso.')
    return True

# Cria uma nova conta corrente associada a um usuário já existente
@decorador_de_log
def criar_conta_corrente(cliente: Cliente) -> ContaCorrente:
    # Optei por determinar o número da nova conta baseado no número da última conta da lista ao invés do tamanho da lista(que diminuiria em caso de exclusão de uma conta,
    # levando a criação de contas com o mesmo número)
    numero_conta = 1 if len(contas) == 0 else contas[-1].numero + 1
    nova_conta = ContaCorrente(numero=numero_conta, cliente=cliente)
    return nova_conta

# Lida com o registro de novas contas corrente
def registrar_nova_conta(cliente: Cliente) -> None:
    nova_conta = criar_conta_corrente(cliente)
    contas.append(nova_conta)
    cliente.adicionar_conta(nova_conta)
    print(f'\nNova conta corrente criada: Agência: {nova_conta.agencia}, Conta: {nova_conta.numero}')

# Lida com a desativação de contas, que é zerada caso ainda possua saldo
def desativar_conta(*, agencia: str, numero_conta: str, lista_contas_usuario: list[Conta]) -> bool:
    conta = encontrar_uma_conta(agencia=agencia, numero_conta=numero_conta, lista_contas=lista_contas_usuario)
    if conta == 'conta nao encontrada':
        return False
    else:
        if conta.saldo > 0:
            saque_final(conta=conta)
        conta.desativar_conta()
        return True

# Encontra todas as contas ativas de um cliente as retorna em uma lista
def encontrar_contas_ativas(contas: list[Conta]) -> list[Conta]:
    lista_contas_usuario = []
    for conta in contas:
        if conta.ativa:
            lista_contas_usuario.append(conta)
    
    return lista_contas_usuario

# Encontra e retorna uma conta de acordo com o numero da agencia e o numero da conta
def encontrar_uma_conta(*, agencia: str, numero_conta: str, lista_contas: list[Conta] = contas) -> Conta | str:
    for conta in lista_contas:
        if conta.agencia == agencia and str(conta.numero) == numero_conta:
            return conta
    print('\nConta não encontrada.')
    return 'conta nao encontrada'

# Pega uma lista de contas e formata em uma string
def listar_contas(contas_usuario: list[Conta]) -> str:
    res = ''
    for conta in ContaIterador(contas_usuario):
        res += conta
    return res

def alterar_limite_saque_geral() -> bool:
    
    @decorador_de_log
    def atualizar_limite_saque(novo_limite):
        global LIMITE_SAQUE
        LIMITE_SAQUE = round(novo_limite, 2)

    LIMITE_MINIMO_SAQUE = 100
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        novo_limite = input(f'Insira o novo valor limite de saque(Valor mínimo: R$ {LIMITE_MINIMO_SAQUE:.2f}) ou "sair" caso deseje abortar a operação: R$ ')
        if novo_limite == 'sair':
            return True
        try:
            novo_limite = float(novo_limite)
            if novo_limite < LIMITE_MINIMO_SAQUE:
                raise ValueError('\nValor passado é menor que o limite mínimo.')
            atualizar_limite_saque(novo_limite)
            for conta in contas:
                conta.limite = LIMITE_SAQUE
            print(f'\nValor limite de saque atualizado para R$ {LIMITE_SAQUE:.2f}')
            return True
        except ValueError as err:
            tentativas += 1
            if err.args[0] == f"could not convert string to float: '{novo_limite}'":
                print(f'\nInsira um número de ponto flutuante maior que {LIMITE_MINIMO_SAQUE}.')
            else:
                print(err.args[0])
            print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return False

def alterar_limite_saque_uma_conta() -> bool:
    if len(contas) == 0:
        print('\nNenhuma conta encontrada na base de dados. Recurso indisponível.')
        return True
    LIMITE_MINIMO_SAQUE = 100
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print('\nInsira as informações da conta ou "sair" caso deseje abortar a operção a qualquer momento:')
        agencia = input('Agência: ')
        if agencia == 'sair':
            return True
        numero_conta = input('Número da conta: ')
        if numero_conta == 'sair':
            return True
        conta = encontrar_uma_conta(agencia=agencia, numero_conta=numero_conta)
        if conta == 'conta nao encontrada':
            tentativas += 1
            print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            continue
        while tentativas < MAX_TENTATIVAS:
            novo_limite = input(f'\nInsira o novo valor limite de saque(Valor mínimo: R$ {LIMITE_MINIMO_SAQUE:.2f}): R$ ')
            if novo_limite == 'sair':
                return True
            try:
                novo_limite = float(novo_limite)
                if novo_limite < LIMITE_MINIMO_SAQUE:
                    raise ValueError('\nValor passado é menor que o limite mínimo.')
                else:
                    conta.limite = novo_limite
                    print(f'\nValor limite de saque da Conta {conta.numero}, Agência {conta.agencia} atualizado para R$ {novo_limite:.2f}')
                    return True
            except ValueError as err:
                tentativas += 1
                if err.args[0] == f"could not convert string to float: '{novo_limite}'":
                    print(f'\nInsira um número de ponto flutuante maior ou igual a {LIMITE_MINIMO_SAQUE}.')
                else:
                    print(err.args[0])
                print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return False

# Altera o limite de saques diário de todas as contas
def alterar_limite_saques_diarios_geral() -> bool:

    @decorador_de_log
    def atualizar_limite_saques_diarios(novo_limite):
        global LIMITE_SAQUES_DIARIOS
        LIMITE_SAQUES_DIARIOS = novo_limite

    LIMITE_MINIMO_SAQUES_DIARIOS = 1
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        novo_limite = input(f'\nInsira o novo limite de saques diários(valor mínimo: {LIMITE_MINIMO_SAQUES_DIARIOS}) ou "sair" para abortar a operação: ')
        if novo_limite == 'sair':
            return True
        try:
            novo_limite = int(novo_limite)
            if novo_limite < LIMITE_MINIMO_SAQUES_DIARIOS:
                raise ValueError('Valor menor que 1')
            atualizar_limite_saques_diarios(novo_limite)
            for conta in contas:
                if isinstance(conta, ContaCorrente):
                    conta.limite_saques = novo_limite
            print('\nLimite de saques diário de todas as contas alterado.')
            return True
        except ValueError as err:
            tentativas += 1
            print(f"\nInsira um valor inteiro maior ou igual a {LIMITE_MINIMO_SAQUES_DIARIOS}")
            print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return False

# Altera o limite de saques diários de uma única conta
def alterar_limite_saques_diarios_uma_conta() -> bool:
    if len(contas) == 0:
        print("\nNenhuma conta encontrada. Recurso indisponível.")
        return True
    LIMITE_MINIMO_SAQUES_DIARIOS = 1
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print('\nCaso deseje abortar a operação, insira "sair" em qualquer um dos campos solicitados.')
        agencia = input('Insira o número da agência: ')
        if agencia == 'sair':
            return True
        numero_conta = input('Insira o número da conta: ')
        if numero_conta == 'sair':
            return True
        conta = encontrar_uma_conta(agencia=agencia, numero_conta=numero_conta)
        if conta == 'conta nao encontrada':
            tentativas += 1
            print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
        else:
            while tentativas < MAX_TENTATIVAS:
                novo_limite = input(f'Insira o novo limite de saques diários(valor mínimo: {LIMITE_MINIMO_SAQUES_DIARIOS}): ')
                if novo_limite == 'sair':
                    return True
                try:
                    novo_limite = int(novo_limite)
                    if novo_limite < LIMITE_MINIMO_SAQUES_DIARIOS:
                        raise ValueError('Valor menor que 1')
                    else:
                        conta.limite_saques = novo_limite
                        print(f"\nLimite de saques diários da Agencia: {agencia}, Conta: {numero_conta} alterado para {novo_limite}.")
                        return True
                except ValueError as err:
                    tentativas += 1
                    print(f"\nInsira um valor inteiro maior ou igual a {LIMITE_MINIMO_SAQUES_DIARIOS}")
                    print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return False

# Exclui uma conta desativada
def excluir_conta_desativada() -> bool:
    
    @decorador_de_log
    def deletar_conta_desativada(index, conta):
        conta.cliente.contas.remove(conta)
        del contas[index]
    
    ha_contas_desativadas = verificar_contas_desativadas()
    if not ha_contas_desativadas:
        print('\nNenhuma conta desativada encontrada. Recurso indisponível.')
        return True
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print('\nInsira as informações da conta ou "sair" caso deseje abortar a operação:')
        agencia = input('Agência: ')
        if agencia == 'sair':
            return True
        numero_conta = input('Número da conta: ')
        if numero_conta == 'sair':
            return True
        conta_encontrada = False
        for i, conta in enumerate(contas):
            if conta.agencia == agencia and str(conta.numero) == numero_conta:
                conta_encontrada = True
                if conta.ativa:
                    tentativas += 1
                    print(f'\nConta ativa. Contas ativas não podem ser excluídas.')
                    print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                    break
                else:
                    # Remove a conta da lista interna do cliente e da lista geral
                    deletar_conta_desativada(i, conta)
                    print(f'\nConta {numero_conta}, Agencia {agencia} foi excluída com sucesso.')
                    return True
        if not conta_encontrada:    
            tentativas += 1
            print(f'\nConta não encontrada.')
            print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    
    return False

def encontrar_cliente_excluir_contas_desativadas() -> bool:
    ha_contas_desativadas = verificar_contas_desativadas()
    if not ha_contas_desativadas:
        print('\nNenhuma conta desativada encontrada. Recurso indisponível.')
        return True
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        identificacao = input('\nInsira o CPF ou CNPJ(somente os números) do usuário a ser excluído ou "sair" para abortar a operação: ')
        if identificacao == 'sair':
            return True
        
        try:
            int(identificacao)
            if len(identificacao) == 11:
                cliente = verificar_cpf(identificacao)
            elif len(identificacao) == 14:
                cliente = verificar_cnpj(identificacao)
            else:
                raise ValueError('\nInsira um número que contenha 11 dígitos(CPF) ou 14 dígitos(CNPJ).')
            
            if cliente == None:
                raise ValueError('\nCliente não encontrado.')
            else:
                excluir_todas_contas_desativadas_de_um_usuario(cliente)
                return True
        except ValueError as err:
            tentativas += 1
            if err.args[0] == f"invalid literal for int() with base 10: '{identificacao}'":
                print('\nInsira somente os números do CPF ou do CNPJ do usuário a ser excluído.')
            else:
                print(err.args[0])
            print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
    return False



# Exclui todas as contas desativadas de um usuario
@decorador_de_log
def excluir_todas_contas_desativadas_de_um_usuario(cliente: Cliente) -> None:
    # Percorre a lista de contas ao contrário para que a exclusão de uma conta não afete o índice da próxima conta a ser excluída
    # Exclui as contas desativadas do usuário da lista geral de contas
    for i in range(len(contas) - 1, -1, -1):
        if contas[i].cliente == cliente and not contas[i].ativa:
            del contas[i]
    # Exclui as contas desativadas do usuário da lista interna dele de contas
    for j in range(len(cliente.contas) - 1, -1, -1):
        if not cliente.contas[j].ativa:
            del cliente.contas[j]

    print(f'\nTodas as contas desativadas do usuário {cliente.nome} foram excluídas.')

# Exclui todas as contas desativadas
@decorador_de_log
def excluir_todas_contas_desativadas() -> bool:
    ha_contas_desativadas = verificar_contas_desativadas()
    if not ha_contas_desativadas:
        print('\nNenhuma conta desativada encontrada. Recurso indisponível.')
        return True
    # Percorre a lista de contas ao contrário para que a exclusão de uma conta não afete o índice da próxima conta a ser excluída
    print()
    for i in range(len(contas) - 1, -1, -1):
        if not contas[i].ativa:
            print(f"Agencia {contas[i].agencia}, Conta {contas[i].numero} excluída com sucesso")
            contas[i].cliente.contas.remove(contas[i])
            del contas[i]
    print('\nTodas as contas desativadas foram excluídas com sucesso.')
    return True

# Verifica se há contas desativadas
def verificar_contas_desativadas() -> bool:
    for conta in contas:
        if not conta.ativa:
            return True
    return False

# Lida com o registro de novos usuários
def cadastrar_usuario(cpf_cnpj: str, tipo: str) -> None:
    MENU_CADASTRO_CLIENTE = '''
[1] Cadastrar
[0] Sair
'''
    print(f"\nVerificamos que o {tipo} informado não está cadastrado no nosso banco de dados de clientes. Gostaria de se cadastrar?")
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print(MENU_CADASTRO_CLIENTE)
        opcao = input('Escolha uma das opções: ')
        if opcao == '1':
            if tipo == 'CPF':
                novo_usuario = criar_usuario_pf(cpf_cnpj)
            elif tipo == 'CNPJ':
                novo_usuario = criar_usuario_pj(cpf_cnpj)
            # Se alguma das etapas da criação do novo usuário falhar por número máximo de tentativas excedido, o atendimento é terminado
            if novo_usuario == None:    
                tentativas = MAX_TENTATIVAS
                break
            # Se a criação do novo usuário for bem sucedida, o usuário é levado para o menu de contas
            else:
                usuarios.append(novo_usuario)
                print('\nCadastro realizado com sucesso. Obrigado por se tornar nosso cliente!')
                gerenciar_contas(novo_usuario)
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
def movimentar_contas(*, conta_escolhida: Conta) -> str:
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print()
        print('Movimentação de contas'.center(60, '-'))
        MENU_OPERACOES = f'''
Agencia: {conta_escolhida.agencia} Conta: {conta_escolhida.numero}
Saldo: R$ {conta_escolhida.saldo:.2f}
Operações Restantes Hoje: {conta_escolhida.limite_transacoes - conta_escolhida.transacoes_hoje}

[1] Saque {'- INDISPONÍVEL' if conta_escolhida.saldo <= 0 or conta_escolhida.saques_hoje >= conta_escolhida.limite_saques or conta_escolhida.transacoes_hoje >= conta_escolhida.limite_transacoes else ''}
[2] Depósito {'- INDISPONÍVEL' if conta_escolhida.transacoes_hoje >= conta_escolhida.limite_transacoes else ''}
[3] Extrato
[0] Sair
'''
        print(MENU_OPERACOES)
        opcao = input('Escolha uma das opções: ')
        # Efetuar saque
        if opcao == '1':
            if conta_escolhida.transacoes_hoje >= conta_escolhida.limite_transacoes:
                print(f'\nLimite de {conta_escolhida.limite_transacoes} transações diárias atingido, operação não efetuada.')
                tentativas += 1
                print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            # Não permite mais saques do que o limite diário da conta
            elif conta_escolhida.saques_hoje >= conta_escolhida.limite_saques:
                print('\nLimite de saques diários atingido, operação não efetuada.')
                tentativas += 1
                print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            # Não permite efetuar saques em contas sem saldo
            elif conta_escolhida.saldo <= 0:
                print('\nSaldo insuficiente.')
                tentativas += 1
                print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            else:
                sucesso = gerenciar_tentativas_saque(conta_escolhida)
                if sucesso:
                    tentativas = 0
                else:
                    return 'tentativas excedidas'

        # Efetuar depósito
        elif opcao == '2':
            if conta_escolhida.transacoes_hoje >= conta_escolhida.limite_transacoes:
                print(f'\nLimite de {conta_escolhida.limite_transacoes} transações diárias atingido, operação não efetuada.')
                tentativas += 1
                print(f'Tentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            else:
                sucesso = gerenciar_tentativas_deposito(conta_escolhida)
                if sucesso:
                    tentativas = 0
                else:
                    return 'tentativas excedidas'
        # Imprimir extrato
        elif opcao == '3':
            sucesso = menu_extrato(conta_escolhida=conta_escolhida)
            if sucesso:
                tentativas = 0
            else: 
                tentativas = MAX_TENTATIVAS
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

def menu_extrato(*, conta_escolhida: Conta):
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print()
        print('Menu Extrato'.center(60, '-'))
        MENU_OPERACOES = f'''
Agencia: {conta_escolhida.agencia} Conta: {conta_escolhida.numero}
Saldo: R$ {conta_escolhida.saldo:.2f}

[1] Extrato completo
[2] Somente saques
[3] Somente depósitos
[0] Sair
'''
        print(MENU_OPERACOES)
        opcao = input('Escolha uma das opções: ')
        if opcao == '1':
            exibir_extrato(conta_escolhida.saldo, agencia=conta_escolhida.agencia, numero=conta_escolhida.numero, titular=conta_escolhida.cliente.nome, historico=conta_escolhida.historico)
            tentativas = 0
        elif opcao == '2':
            exibir_saques(conta_escolhida.saldo, agencia=conta_escolhida.agencia, numero=conta_escolhida.numero, titular=conta_escolhida.cliente.nome, historico=conta_escolhida.historico)
            tentativas = 0
        elif opcao == '3':
            exibir_depositos(conta_escolhida.saldo, agencia=conta_escolhida.agencia, numero=conta_escolhida.numero, titular=conta_escolhida.cliente.nome, historico=conta_escolhida.historico)
            tentativas = 0
        elif opcao == '0':
            return True
        else:
            tentativas += 1
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')

    return False


# Função responsável pelas opções do menu de gerenciamento de contas, ou seja, criação, movimentação e desativação de contas corrente e desativação de usuário
def gerenciar_contas(cliente: Cliente) -> None:
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print()
        print('Gerenciamento de contas'.center(60, '-'))
        contas_usuario = encontrar_contas_ativas(cliente.contas)
        contas_formatadas = listar_contas(contas_usuario)
        possui_contas = len(contas_usuario) != 0
        MENU_CONTAS = f'''
[1] Criar nova conta corrente
[2] Movimentar conta corrente {'- INDISPONÍVEL' if not possui_contas else ''}
[3] Desativar conta corrente {'- INDISPONÍVEL' if not possui_contas else ''}
[4] Desativar usuário {'- INDISPONÍVEL' if possui_contas else ''}
[0] Sair
'''
        print(f"\n{'Suas contas:' if len(contas_usuario) > 0 else 'Nenhuma conta registrada.'}" + f'\n{contas_formatadas}' + MENU_CONTAS)
        opcao = input('Escolha uma das opções: ')
        # Abrir nova conta corrente
        if opcao == '1':
            registrar_nova_conta(cliente)
            tentativas = 0
            print('\nComo mais podemos ajudá-lo?')
        # Movimentar conta corrente
        elif opcao == '2':
            if possui_contas:
                print('\nInsira os dados da conta que deseja movimentar.')
                agencia = input('Agência: ')
                numero_conta = input('Número da conta: ')
                conta = encontrar_uma_conta(agencia=agencia, numero_conta=numero_conta, lista_contas=contas_usuario)
                if conta == 'conta nao encontrada':
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
                else:
                    res = movimentar_contas(conta_escolhida=conta)
                    if res == 'operacao bem sucedida':
                        tentativas = 0
                        print('\nComo mais podemos ajudá-lo?')
                    elif res == 'tentativas excedidas':
                        tentativas = MAX_TENTATIVAS
            else:
                print('\nNenhuma conta ativa encontrada.')
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
        # Desativar Conta Corrente
        elif opcao == '3':
            if possui_contas:   
                print('\nInsira os dados da conta que deseja desativar.')
                agencia = input('Agência: ')
                numero_conta = input('Número da conta: ')
                conta_desativada = desativar_conta(agencia=agencia, numero_conta=numero_conta, lista_contas_usuario=contas_usuario)
                # Conta desativada com sucesso
                if conta_desativada:
                    tentativas = 0
                    print('\nComo mais podemos ajudá-lo?')
                else:
                    tentativas += 1
                    print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
            else:
                print('\nNenhuma conta ativa encontrada.')
                tentativas += 1
                print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
        # Desativar Usuário
        elif opcao == '4':
            if not possui_contas:
                cliente.desativar_conta_cliente()
                print('\nLamentamos que esteja de saída.')
                break
            else:
                tentativas += 1
                print('\nNão podemos excluir o usuário atual enquanto houver contas ativas vinculadas ao mesmo.')
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
def gerenciamento_institucional() -> None:
    LIMITE_MINIMO_SAQUE = 100.0
    global MAX_TENTATIVAS, LIMITE_SAQUE, LIMITE_SAQUES_DIARIOS
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        ha_contas_desativadas = verificar_contas_desativadas()
        ha_usuarios_desativados = verificar_usuarios_desativados()
        print()
        print(' GERENCIAMENTO INSTITUCIONAL '.center(100, 'X'))
        print()
        imprimir_clientes()
        imprimir_contas()
        MENU_GERENCIAMENTO = f'''
[1] Alterar o limite de saques diários de todas as contas
[2] Alterar o limite de saques diários de uma conta {'- INDISPONÍVEL' if len(contas) == 0 else ''}
[3] Excluir usuário desativado {'- INDISPONÍVEL' if not ha_usuarios_desativados else ''}
[4] Excluir todos os usuários desativados {'- INDISPONÍVEL' if not ha_usuarios_desativados else ''}
[5] Excluir todas as contas desativadas de um usuário {'- INDISPONÍVEL' if not ha_contas_desativadas else ''}
[6] Excluir conta desativada {'- INDISPONÍVEL' if not ha_contas_desativadas else ''}
[7] Excluir todas as contas desativadas {'- INDISPONÍVEL' if not ha_contas_desativadas else ''}
[8] Alterar valor limite de saque
[9] Alterar valor limite de saque de uma conta {'' if len(contas) > 0 else '- INDISPONÍVEL'}
[10] Exibir extrato de uma conta {'' if len(contas) > 0 else '- INDISPONÍVEL'}
[0] Sair
'''
        OPCOES = {
            '1': alterar_limite_saques_diarios_geral,
            '2': alterar_limite_saques_diarios_uma_conta,
            '3': excluir_usuario_desativado,
            '4': excluir_todos_usuarios_desativados,
            '5': encontrar_cliente_excluir_contas_desativadas,
            '6': excluir_conta_desativada,
            '7': excluir_todas_contas_desativadas,
            '8': alterar_limite_saque_geral,
            '9': alterar_limite_saque_uma_conta,
            '10': exibir_extrato_de_uma_conta
        }
        print(MENU_GERENCIAMENTO)
        opcao = input('Escolha uma das opções: ')
        if opcao == '0':
            break
        escolha = OPCOES.get(opcao, None)
        if escolha != None:
            acao_bem_sucedida = escolha()
            if acao_bem_sucedida:
                tentativas = 0
            else:
                print('\nLimite de tentativas excedido.')
                break
        # Input não corresponde a nenhuma das opções
        else:
            tentativas += 1
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')
        # Input que não corresponde a nenhuma das opções disponíveis inserido 3 vezes seguidas
        if tentativas >= MAX_TENTATIVAS:
            print('Número máximo de tentativas excedido.')

# Atendimento de pessoas físicas 
def atendimento_pessoa_fisica() -> None:
    cpf = solicitar_cpf()
    # Se o cpf for informado no formato correto
    if cpf != 'sair':
        # Verifica se o cpf já está cadastrado
        cliente = verificar_cpf(cpf)
        if cliente != None:
            # Vai para o menu de gerenciamento de contas
            if not cliente.ativo:
                cliente_reativado = reativacao_cliente(cliente)
                # Se o cliente for reativado, vai para o gerenciamento de contas, se não a sessão é encerrada
                if cliente_reativado:
                    gerenciar_contas(cliente)
            else:
                gerenciar_contas(cliente)
        else:
            # Cadastra o usuário
            cadastrar_usuario(cpf, 'CPF')
    
    print('\nObrigado por utilizar os nossos serviços!')

# Atendimento de pessoas jurídicas
def atendimento_pessoa_juridica() -> None:
    cnpj = solicitar_cnpj()
    # Se o cnpj for informado no formato correto
    if cnpj != 'sair':
        # verifica se o cnpj já está cadastrado
        cliente = verificar_cnpj(cnpj)
        if cliente != None:
            # Vai para o menu de gerenciamento de contas
            if not cliente.ativo:
                cliente_reativado = reativacao_cliente(cliente)
                # Se o cliente for reativado, vai para o gerenciamento de contas, se não a sessão é encerrada
                if cliente_reativado:
                    gerenciar_contas(cliente)
            else:
                gerenciar_contas(cliente)
        else: 
            # Cadastrar cliente
            cadastrar_usuario(cnpj, 'CNPJ')
    
    print('\nObrigado por utilizar os nossos serviços!')

# Inicio do programa
def iniciar_atendimento() -> None:
    carregar_usuarios()
    carregar_contas()
    MENSAGEM_INICIAL = '''
Bem vindo(a) ao Banco X!
    
[1] Pessoa Física
[2] Pessoa Jurídica
[0] Sair
'''
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        print(f"\n{''.center(100, 'X')}")
        print(MENSAGEM_INICIAL)
        opcao = input('Escolha uma das opções: ')
        if opcao == '1':
            tentativas = 0
            atendimento_pessoa_fisica()
        elif opcao == '2':
            tentativas = 0
            atendimento_pessoa_juridica()
            pass
        elif opcao == '0':
            break
        # Acesso ao menu de gerenciamento do banco, que permite exclusão permanente de usuários e contas corrente desativados, bem como a reinicialização dos saques diários
        # de contas individuais ou de todas
        elif opcao == '99':
            tentativas = 0
            gerenciamento_institucional()
        else:
            tentativas += 1
            print(f'\nTentativas Restantes: {MAX_TENTATIVAS - tentativas}')

    if tentativas >= MAX_TENTATIVAS:
        print('Número máximo de tentativas excedido.')
    print('\nObrigado por utilizar os nossos serviços!\n')
    salvar_usuarios()
    salvar_contas()


if __name__ == '__main__':
    iniciar_atendimento()
