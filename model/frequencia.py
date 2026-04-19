# model/frequencia.py
# Classe Frequencia - Composição com Matricula (Matricula compõe Frequencias)
# Associação 0..*:1 com Materia (Frequencia referente a Materia)
# RF06 atualizado: registra presença E falta, professor pode editar dia anterior

from datetime import date


class Frequencia:
    """Registro de frequência de um aluno em uma aula."""

    def __init__(
        self,
        data_aula: date = None,
        presente: bool = False,
        justificativa: str = ""
    ):
        # Atributos protegidos conforme diagrama
        self._data_aula: date = data_aula
        self._presente: bool = presente
        self._justificativa: str = justificativa
        # Novos atributos RF06: controle de edição
        self._data_registro: date = date.today()   # Data em que o registro foi feito
        self._editado: bool = False                 # Indica se o registro foi editado
        self._data_edicao: date = None               # Data da última edição
        # Associação 0..*:1 com Materia
        self._materia = None

    # --- Getters e Setters ---

    @property
    def data_aula(self) -> date:
        return self._data_aula

    @data_aula.setter
    def data_aula(self, valor: date):
        self._data_aula = valor

    @property
    def presente(self) -> bool:
        return self._presente

    @presente.setter
    def presente(self, valor: bool):
        self._presente = valor

    @property
    def justificativa(self) -> str:
        return self._justificativa

    @justificativa.setter
    def justificativa(self, valor: str):
        self._justificativa = valor

    @property
    def data_registro(self) -> date:
        return self._data_registro

    @property
    def editado(self) -> bool:
        return self._editado

    @property
    def data_edicao(self) -> date:
        return self._data_edicao

    @property
    def materia(self):
        return self._materia

    @materia.setter
    def materia(self, valor):
        self._materia = valor

    # --- Métodos públicos (diagrama de classes) ---

    def registrar_presenca(self) -> None:
        """Registra presença do aluno na aula (RF06)."""
        self._presente = True
        self._data_registro = date.today()

    def registrar_falta(self, justificativa: str = "") -> None:
        """Registra falta do aluno na aula (RF06).
        Args:
            justificativa: motivo da falta (opcional).
        """
        self._presente = False
        self._justificativa = justificativa
        self._data_registro = date.today()

    def editar_registro(self, presente: bool, justificativa: str = "") -> None:
        """Edita o registro de frequência (RF06 - correção de erro).
        Args:
            presente: novo valor de presença.
            justificativa: nova justificativa (se falta).
        """
        self._presente = presente
        self._justificativa = justificativa
        self._editado = True
        self._data_edicao = date.today()

    def validar_edicao(self, data_aula: date) -> bool:
        """Valida se a edição é permitida (RF06 - apenas dia anterior).
        Args:
            data_aula: data da aula a ser editada.
        Returns:
            True se a data é anterior a hoje (permite edição).
        """
        return data_aula < date.today()
