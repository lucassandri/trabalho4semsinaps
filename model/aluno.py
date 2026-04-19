# model/aluno.py
# Classe Aluno - herda de Pessoa (Herança)
# Composição 1:0..* com Matricula (Aluno compõe Matriculas)
# Agregação 1:0..* com HistoricoEscolar (Aluno possui HistoricoEscolar)

from datetime import date
from model.pessoa import Pessoa


class Aluno(Pessoa):
    """Aluno da escola. Consulta boletim e histórico (RF09)."""

    def __init__(
        self,
        nome: str = "",
        cpf: str = "",
        data_nascimento: date = None,
        telefone: str = "",
        email: str = "",
        endereco: str = "",
        matricula_aluno: str = "",
        data_matricula: date = None,
        responsavel: str = "",
        telefone_responsavel: str = ""
    ):
        # Inicializa atributos herdados de Pessoa
        super().__init__(nome, cpf, data_nascimento, telefone, email, endereco)
        # Atributos protegidos conforme diagrama
        self._matricula_aluno: str = matricula_aluno
        self._data_matricula: date = data_matricula
        self._responsavel: str = responsavel
        self._telefone_responsavel: str = telefone_responsavel
        # Composição 1:0..* com Matricula
        self._matriculas: list = []
        # Agregação 1:0..* com HistoricoEscolar
        self._historicos: list = []

    # --- Getters e Setters ---

    @property
    def matricula_aluno(self) -> str:
        return self._matricula_aluno

    @matricula_aluno.setter
    def matricula_aluno(self, valor: str):
        self._matricula_aluno = valor

    @property
    def data_matricula(self) -> date:
        return self._data_matricula

    @data_matricula.setter
    def data_matricula(self, valor: date):
        self._data_matricula = valor

    @property
    def responsavel(self) -> str:
        return self._responsavel

    @responsavel.setter
    def responsavel(self, valor: str):
        self._responsavel = valor

    @property
    def telefone_responsavel(self) -> str:
        return self._telefone_responsavel

    @telefone_responsavel.setter
    def telefone_responsavel(self, valor: str):
        self._telefone_responsavel = valor

    @property
    def matriculas(self) -> list:
        return self._matriculas

    @property
    def historicos(self) -> list:
        return self._historicos

    # --- Métodos públicos (diagrama de classes) ---

    def consultar_boletim(self, matricula):
        """Consulta boletim de uma matrícula específica (RF09).
        Args:
            matricula: objeto Matricula.
        Returns:
            Objeto Boletim ou None.
        """
        if matricula in self._matriculas:
            return matricula.boletim
        return None

    def consultar_historico(self):
        """Consulta histórico escolar do aluno (RF09).
        Returns:
            Último HistoricoEscolar ou None.
        """
        if self._historicos:
            return self._historicos[-1]
        return None

    def adicionar_matricula(self, matricula) -> None:
        """Adiciona matrícula ao aluno (Composição: aluno compõe matrícula)."""
        if matricula not in self._matriculas:
            self._matriculas.append(matricula)

    def remover_matricula(self, matricula) -> None:
        """Remove matrícula do aluno (Composição: destrói a parte)."""
        if matricula in self._matriculas:
            self._matriculas.remove(matricula)

    def adicionar_historico(self, historico) -> None:
        """Adiciona histórico escolar ao aluno (Agregação)."""
        if historico not in self._historicos:
            self._historicos.append(historico)
