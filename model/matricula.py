# model/matricula.py
# Classe Matricula - Composição:
#   Compõe: Boletim (1:1), Frequencia (1:0..*)
# É composta por: Aluno e Turma

from datetime import date


class Matricula:
    """Matrícula de um aluno em uma turma."""

    def __init__(
        self,
        codigo: str = "",
        data_matricula: date = None,
        status: str = "ativa"
    ):
        # Atributos protegidos conforme diagrama
        self._codigo: str = codigo
        self._data_matricula: date = data_matricula
        self._status: str = status
        self._data_transferencia: date = None
        self._data_cancelamento: date = None
        # Composição 1:1 com Boletim
        self._boletim = None
        # Composição 1:0..* com Frequencia
        self._frequencias: list = []

    # --- Getters e Setters ---

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str):
        self._codigo = valor

    @property
    def data_matricula(self) -> date:
        return self._data_matricula

    @data_matricula.setter
    def data_matricula(self, valor: date):
        self._data_matricula = valor

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, valor: str):
        self._status = valor

    @property
    def data_transferencia(self) -> date:
        return self._data_transferencia

    @property
    def data_cancelamento(self) -> date:
        return self._data_cancelamento

    @property
    def boletim(self):
        return self._boletim

    @boletim.setter
    def boletim(self, valor):
        self._boletim = valor

    @property
    def frequencias(self) -> list:
        return self._frequencias

    # --- Métodos públicos (diagrama de classes) ---

    def cancelar(self) -> None:
        """Cancela esta matrícula (RF02)."""
        self._status = "cancelada"
        self._data_cancelamento = date.today()

    def transferir(self, turma_destino) -> None:
        """Transfere matrícula para outra turma (RF02).
        Args:
            turma_destino: objeto Turma de destino.
        """
        self._status = "transferida"
        self._data_transferencia = date.today()

    def criar_boletim(self):
        """Cria o boletim associado a esta matrícula (Composição).
        Returns:
            Objeto Boletim criado.
        """
        from model.boletim import Boletim
        self._boletim = Boletim()
        return self._boletim

    def adicionar_frequencia(self, frequencia) -> None:
        """Adiciona registro de frequência (Composição).
        Args:
            frequencia: objeto Frequencia.
        """
        self._frequencias.append(frequencia)
