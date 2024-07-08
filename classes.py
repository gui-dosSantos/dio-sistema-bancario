from pathlib import Path
from datetime import datetime, date
from abc import ABC, abstractmethod
import functools

ROOT_PATH = Path(__file__).parent

LIMITE_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3

def decorador_de_log(func):
    @functools.wraps(func)
    def envelope(*args, **kwargs):
        data_hora = args[0].data.strftime('%d/%m/%Y %H:%M:%S')
        nome_func = f'{args[0].__class__.__name__}.{func.__name__}'
        retorno = func(*args, **kwargs)
        try:
            with open(ROOT_PATH / 'log.txt', 'a', encoding='utf-8') as log:
                log.write(f'{data_hora} - {nome_func}{args} -> {retorno}\n')
        except IOError as err:
            print('Erro ao abrir o arquivo.')

        print(f"\nOperação: {args[0].tipo}\nHorário: {data_hora}")

    return envelope

class ContaIterador:
    def __init__(self, contas,/ , *, extendido: bool = False) -> None:
        self.contas = contas
        self.contador = 0
        self.extendido = extendido
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self.contador]
            self.contador += 1
            if self.extendido:
                return f'Agencia: {conta.agencia} - Número: {conta.numero} - Titular: {conta.cliente.nome} - Saldo: R$ {conta.saldo:.2f} - Ativa: {conta.ativa}'
            else:
                return f'Agência: {conta.agencia}, Conta: {conta.numero}, Saldo: R$ {conta.saldo:.2f}\n'
        except IndexError:
            raise StopIteration    

class Conta:
    def __init__(self, *, numero: int, cliente) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
        self._ativa = True
        self._limite_transacoes = 10
    
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
    
    @property
    def ativa(self):
        return self._ativa
    
    @property
    def limite_transacoes(self):
        return self._limite_transacoes

    @property
    def transacoes_hoje(self):
        transacoes_hoje = 0
        for transacao in self.historico.transacoes:
            if transacao.data.date() == date.today():
                transacoes_hoje += 1
        return transacoes_hoje

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero=numero, cliente=cliente)
    
    def desativar_conta(self):
        self._ativa = False
    
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

    # Saque de encerramento de conta, que zera o saldo caso este seja maior que 0
    def saque_final(self):
        valor = self.saldo
        self._saldo -= valor
        print(f'\nSaque final no valor de R$ {valor:.2f} efetuado com sucesso.')

    def __repr__(self) -> str:
        return f'Conta: \"Agencia: {self.agencia}, Número: {self.numero}, Cliente: {self.cliente.nome}\"'

    def __str__(self) -> str:
        return f'Agencia: {self.agencia} - Número: {self.numero} - Titular: {self.cliente.nome} - Saldo: {self.saldo} - Ativa: {self.ativa}'

class ContaCorrente(Conta):
    global LIMITE_SAQUE, LIMITE_SAQUES_DIARIOS

    def __init__(self, *, numero: int, cliente, limite: float = LIMITE_SAQUE, limite_saques: int = LIMITE_SAQUES_DIARIOS) -> None:
        super().__init__(numero=numero, cliente=cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite
    
    @limite.setter
    def limite(self, value):
        self._limite = value
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    @limite_saques.setter
    def limite_saques(self, value):
        self._limite_saques = value
    
    # Verifica quantos saques foram realizados no dia
    @property
    def saques_hoje(self):
        saques_hoje = 0
        for transacao in self.historico.transacoes:
            if transacao.tipo == 'Saque' and transacao.data.date() == date.today():
                saques_hoje += 1
        return saques_hoje
    
    def sacar(self, valor: float) -> bool:
        if self.saques_hoje >= self.limite_saques:
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
        self._tipo = 'Depósito'
        self._data = datetime.now()

    @property
    def valor(self):
        return self._valor
    
    @property
    def tipo(self):
        return self._tipo
    
    @property
    def data(self):
        return self._data

    @decorador_de_log
    def registrar(self, conta: Conta):
        conta.historico.adicionar_transacao(self)

    def __repr__(self) -> str:
        return f'Transação: \"{self.tipo}: {self.valor}\"'

class Saque(Transacao):
    def __init__(self, valor: float, tipo: str = 'Saque') -> None:
        self._valor = valor
        self._tipo = tipo
        self._data = datetime.now()

    @property
    def valor(self):
        return self._valor
    
    @property
    def tipo(self):
        return self._tipo
    
    @property
    def data(self):
        return self._data

    @decorador_de_log
    def registrar(self, conta: Conta):
        conta.historico.adicionar_transacao(self) 

    def __repr__(self) -> str:
        return f'Transação: \"{self.tipo}: {self.valor}\"'

# Saque de encerramento de conta que zera o saldo
class SaqueFinal(Saque):
    def __init__(self, valor: float) -> None:
        super().__init__(valor, 'Saque Final')

    @decorador_de_log
    def registrar(self, conta: Conta):
        conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self) -> None:
        self._transacoes: list[Transacao] = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(transacao)

    def gerador_de_relatorio(self, tipo: str = None):
        for transacao in self.transacoes:
            if tipo == None:
                yield transacao
            elif transacao.tipo == tipo:
                yield transacao

class Cliente:
    def __init__(self, endereco: str) -> None:
        self.endereco = endereco
        self.contas: list[Conta] = []
        self.ativo: bool = True

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

    def desativar_conta_cliente(self):
        self.ativo = False

    def reativar_conta_cliente(self):
        self.ativo = True

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
    
    def __str__(self):
        return f'Nome: {self.nome} - CPF: {self.cpf} - Ativo: {self.ativo}'

class PessoaJuridica(Cliente):
    def __init__(self, *, endereco: str, cnpj: str, nome: str) -> None:
        super().__init__(endereco)
        self._cnpj = cnpj
        self._nome = nome
    
    @property
    def cnpj(self):
        return self._cnpj
    
    @property
    def nome(self):
        return self._nome
    
    def __str__(self):
        return f'Nome: {self.nome} - CNPJ: {self.cnpj} - Ativo: {self.ativo}'
    