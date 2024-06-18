from datetime import datetime
from abc import ABC, abstractmethod

class Conta:
    def __init__(self, *, numero: int, cliente: Cliente) -> None: # type: ignore
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
    def nova_conta(cls, cliente: Cliente, numero: int): # type: ignore
        return cls(numero=numero, cliente=cliente)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def sacar(valor: float) -> bool:
        pass
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def depositar(valor: float) -> bool:
        pass

class ContaCorrente(Conta):
    def __init__(self, *, saldo: float, numero: int, agencia: str, cliente: Cliente, historico: Historico, limite: float, limite_saques: int) -> None: #type: ignore
        super().__init__(saldo=saldo, numero=numero, agencia=agencia, cliente=cliente, historico=historico)
        self._limite = limite
        self._limite_saques = limite_saques

class Transacao(ABC):
    @abstractmethod
    def registrar(conta: Conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def registrar(conta: Conta):
        pass

class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def registrar(conta: Conta):
        pass 

class Historico:
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def adicionar_transacao(transacao: Transacao):
        pass

class Cliente:
    def __init__(self, endereco: str) -> None:
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, *, endereco: str, cpf: str, nome: str, data_nascimento: datetime) -> None:
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

# c = Cliente(2, 1)
