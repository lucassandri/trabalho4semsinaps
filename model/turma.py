# model/turma.py
# Classe Turma - Composição com Matricula (Turma compõe Matriculas)
# Associação 1:1..* com Materia (Turma oferece Materias)
# RN05: não matricular além da capacidade_maxima (campo RF04)

class Turma:
    """Turma escolar. Controla capacidade e matérias oferecidas."""

    def __init__(
        self,
        codigo: str = "",
        nome: str = "",
        turno: str = "",
        ano_letivo: int = 0,
        capacidade_maxima: int = 0
    ):
        # Atributos protegidos conforme diagrama
        self._codigo: str = codigo
        self._nome: str = nome
        self._turno: str = turno
        self._ano_letivo: int = ano_letivo
        # RN05: capacidade_maxima cadastrada pelo Coordenador (RF04)
        self._capacidade_maxima: int = capacidade_maxima
        self._total_alunos: int = 0
        # Composição 1:0..* com Matricula
        self._matriculas: list = []
        # Associação 1:1..* com Materia
        self._materias: list = []

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
    def turno(self) -> str:
        return self._turno

    @turno.setter
    def turno(self, valor: str):
        self._turno = valor

    @property
    def ano_letivo(self) -> int:
        return self._ano_letivo

    @ano_letivo.setter
    def ano_letivo(self, valor: int):
        self._ano_letivo = valor

    @property
    def capacidade_maxima(self) -> int:
        return self._capacidade_maxima

    @capacidade_maxima.setter
    def capacidade_maxima(self, valor: int):
        self._capacidade_maxima = valor

    @property
    def total_alunos(self) -> int:
        return self._total_alunos

    @property
    def matriculas(self) -> list:
        return self._matriculas

    @property
    def materias(self) -> list:
        return self._materias

    # --- Métodos públicos (diagrama de classes) ---

    def adicionar_matricula(self, matricula) -> bool:
        """Adiciona matrícula à turma (Composição). Respeita RN05.
        Args:
            matricula: objeto Matricula.
        Returns:
            True se adicionou, False se turma cheia.
        """
        # RN05: verifica capacidade antes de adicionar
        if not self.verificar_capacidade():
            return False
        if matricula not in self._matriculas:
            self._matriculas.append(matricula)
            self._total_alunos += 1
        return True

    def remover_matricula(self, matricula) -> None:
        """Remove matrícula da turma (Composição)."""
        if matricula in self._matriculas:
            self._matriculas.remove(matricula)
            self._total_alunos -= 1

    def adicionar_materia(self, materia) -> None:
        """Adiciona matéria à turma (Associação)."""
        if materia not in self._materias:
            self._materias.append(materia)

    def remover_materia(self, materia) -> None:
        """Remove matéria da turma (Associação)."""
        if materia in self._materias:
            self._materias.remove(materia)

    def verificar_capacidade(self) -> bool:
        """Verifica se a turma ainda tem vaga (RN05).
        Returns:
            True se há vaga, False se atingiu capacidade_maxima.
        """
        return self._total_alunos < self._capacidade_maxima
