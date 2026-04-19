# model/pessoa.py
# Classe Pessoa - superclasse de Funcionario e Aluno (Herança)
# Associação 1:1 com Usuario

from datetime import date


class Pessoa:
    """Superclasse que agrupa atributos comuns de Funcionario e Aluno."""

    def __init__(
        self,
        nome: str = "",
        cpf: str = "",
        data_nascimento: date = None,
        telefone: str = "",
        email: str = "",
        endereco: str = ""
    ):
        # Atributos protegidos conforme diagrama de classes
        self._nome: str = nome
        self._cpf: str = cpf
        self._data_nascimento: date = data_nascimento
        self._telefone: str = telefone
        self._email: str = email
        self._endereco: str = endereco
        # Associação 1:1 com Usuario
        self._usuario = None

    # --- Getters e Setters ---

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        self._nome = valor

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str):
        self._cpf = valor

    @property
    def data_nascimento(self) -> date:
        return self._data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, valor: date):
        self._data_nascimento = valor

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, valor: str):
        self._telefone = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        self._email = valor

    @property
    def endereco(self) -> str:
        return self._endereco

    @endereco.setter
    def endereco(self, valor: str):
        self._endereco = valor

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        self._usuario = valor
