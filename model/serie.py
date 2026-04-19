# model/serie.py
# Classe Serie - Composição 1:1..* com Turma (Serie compõe Turmas)

class Serie:
    """Série escolar. Compõe Turmas (composição)."""

    def __init__(self, codigo: str = "", nome: str = "", nivel: str = ""):
        # Atributos protegidos conforme diagrama
        self._codigo: str = codigo
        self._nome: str = nome
        self._nivel: str = nivel
        # Composição 1:1..* com Turma
        self._turmas: list = []

    # --- Getters e Setters ---

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str):
        self._codigo = valor

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        self._nome = valor

    @property
    def nivel(self) -> str:
        return self._nivel

    @nivel.setter
    def nivel(self, valor: str):
        self._nivel = valor

    @property
    def turmas(self) -> list:
        return self._turmas

    # --- Métodos públicos (diagrama de classes) ---

    def adicionar_turma(self, turma) -> None:
        """Adiciona turma a esta série (Composição)."""
        if turma not in self._turmas:
            self._turmas.append(turma)

    def remover_turma(self, turma) -> None:
        """Remove turma desta série (Composição: destrói a parte)."""
        if turma in self._turmas:
            self._turmas.remove(turma)

    def listar_turmas(self) -> list:
        """Lista todas as turmas desta série.
        Returns:
            Lista de objetos Turma.
        """
        return list(self._turmas)
