from datetime import datetime, date
from abc import ABC, abstractmethod

MAX_TENTATIVAS = 3
LIMITE_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3

class Conta:
    def __init__(self, *, numero: int, cliente) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero=numero, cliente=cliente)
    
    # Tentativas, registros e formatos de input devem ser tratados no sistema
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print('\nInsira um valor numérico maior que 0.')
        elif valor > self.saldo:
            print('\nSaldo Insuficiente.')
        else:
            self._saldo -= round(valor, 2)
            print(f'\nSaque no valor de R$ {valor:.2f} efetuado com sucesso.')
            return True            
        
        return False

    # Tentativas, registros e formatos de input devem ser tratados no sistema
    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print('\nInsira um valor numérico maior que 0.')
            return False
        else:
            self._saldo += round(valor, 2)
            print(f'\nDepósito no valor de R$ {valor:.2f} efetuado com sucesso.')
            return True

class ContaCorrente(Conta):
    global LIMITE_SAQUE, LIMITE_SAQUES_DIARIOS

    def __init__(self, *, numero: int, cliente, limite: float = LIMITE_SAQUE, limite_saques: int = LIMITE_SAQUES_DIARIOS) -> None:
        super().__init__(numero=numero, cliente=cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    def sacar(self, valor: float) -> bool:
        # Verifica quantos saques foram realizados no dia
        saques_hoje = 0
        for transacao in self.historico.transacoes:
            if transacao['tipo'] == Saque.__name__ and transacao['data'].date() == date.today():
                saques_hoje += 1
        if saques_hoje >= self.limite_saques:
            print('\nQuantidade máxima de saques diários atingida.')
        elif valor > self.limite:
            print(f'\nO valor limite para saque da sua conta é de R$ {self.limite:.2f}.')
        else:
            return super().sacar(valor)           
        return False

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta: Conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        conta.historico.adicionar_transacao(self) 

class Historico:
    def __init__(self) -> None:
        self._transacoes: list[Transacao] = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        entrada = {
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now()
        }
        self._transacoes.append(entrada)

class Cliente:
    def __init__(self, endereco: str) -> None:
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, *, endereco: str, cpf: str, nome: str, data_nascimento: date) -> None:
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento

