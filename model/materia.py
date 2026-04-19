# model/materia.py
# Classe Materia - classe de dados (sem métodos de negócio)
# Associação com Professor (leciona), Turma (oferece),
# Nota (referente) e Frequencia (referente)

class Materia:
    """Matéria/disciplina escolar."""

    def __init__(self, codigo: str = "", nome: str = "", carga_horaria: int = 0):
        # Atributos protegidos conforme diagrama
        self._codigo: str = codigo
        self._nome: str = nome
        self._carga_horaria: int = carga_horaria

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
    def carga_horaria(self) -> int:
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor: int):
        self._carga_horaria = valor
