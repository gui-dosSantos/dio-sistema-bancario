MENSAGEM_INICIAL = '''
Bem vindo(a) ao Banco X!

Como podemos lhe ajudar?'''
MENU = f'''
{' MENU '.center(20, '-')}

[1] Depósito
[2] Saque
[3] Extrato
[0] Sair

'''

saldo = 0
saques_realizados_hoje = 0
LIMITE_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3
extrato = f"{' EXTRATO '.center(20, '-')}\n\n"

print(MENSAGEM_INICIAL)

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