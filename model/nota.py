# model/nota.py
# Classe Nota - Composição com Boletim (Boletim compõe Notas)
# Associação 0..*:1 com Materia (Nota referente a Materia)
# RN06: notas entre 0.0 e 10.0

from datetime import date


class Nota:
    """Nota bimestral. Compõe o Boletim."""

    def __init__(
        self,
        bimestre: int = 0,
        valor: float = 0.0,
        data_lancamento: date = None
    ):
        # Atributos protegidos conforme diagrama
        self._bimestre: int = bimestre
        self._valor: float = valor
        self._data_lancamento: date = data_lancamento
        # Associação 0..*:1 com Materia
        self._materia = None

    # --- Getters e Setters ---

    @property
    def bimestre(self) -> int:
        return self._bimestre

    @bimestre.setter
    def bimestre(self, valor: int):
        self._bimestre = valor

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, valor: float):
        self._valor = valor

    @property
    def data_lancamento(self) -> date:
        return self._data_lancamento

    @data_lancamento.setter
    def data_lancamento(self, valor: date):
        self._data_lancamento = valor

    @property
    def materia(self):
        return self._materia

    @materia.setter
    def materia(self, valor):
        self._materia = valor

    # --- Métodos públicos (diagrama de classes) ---

    def validar_nota(self) -> bool:
        """Valida se a nota está entre 0.0 e 10.0 (RN06).
        Returns:
            True se válida, False se fora do intervalo.
        """
        return 0.0 <= self._valor <= 10.0
