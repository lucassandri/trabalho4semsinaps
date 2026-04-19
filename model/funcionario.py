# model/funcionario.py
# Classe Funcionario - herda de Pessoa (Herança)
# Superclasse de Professor, Secretaria e Coordenador

from datetime import date
from model.pessoa import Pessoa


class Funcionario(Pessoa):
    """Funcionário da escola. Herda atributos de Pessoa."""

    def __init__(
        self,
        nome: str = "",
        cpf: str = "",
        data_nascimento: date = None,
        telefone: str = "",
        email: str = "",
        endereco: str = "",
        matricula_funcionario: str = "",
        cargo: str = "",
        data_admissao: date = None
    ):
        # Inicializa atributos herdados de Pessoa
        super().__init__(nome, cpf, data_nascimento, telefone, email, endereco)
        # Atributos protegidos conforme diagrama
        self._matricula_funcionario: str = matricula_funcionario
        self._cargo: str = cargo
        self._data_admissao: date = data_admissao

    # --- Getters e Setters ---

    @property
    def matricula_funcionario(self) -> str:
        return self._matricula_funcionario

    @matricula_funcionario.setter
    def matricula_funcionario(self, valor: str):
        self._matricula_funcionario = valor

    @property
    def cargo(self) -> str:
        return self._cargo

    @cargo.setter
    def cargo(self, valor: str):
        self._cargo = valor

    @property
    def data_admissao(self) -> date:
        return self._data_admissao

    @data_admissao.setter
    def data_admissao(self, valor: date):
        self._data_admissao = valor
