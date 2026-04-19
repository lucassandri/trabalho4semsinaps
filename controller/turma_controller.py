# controller/turma_controller.py
# Controller de Turma - opera sobre objetos Turma e o cache

from cache.cache_manager import CacheManager


class TurmaController:
    """Gerencia operações sobre Turma: capacidade, matrículas e matérias."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Consultas ---

    def buscar(self, codigo: str):
        """Busca turma pelo código."""
        return self._cache.buscar_turma(codigo)

    def listar(self) -> list:
        """Lista todas as turmas cadastradas."""
        return self._cache.listar_turmas()

    # --- Capacidade (RN05) ---

    def verificar_capacidade(self, turma) -> bool:
        """Verifica se a turma ainda possui vaga (RN05)."""
        return turma.verificar_capacidade()

    # --- Matrículas compostas ---

    def adicionar_matricula(self, turma, matricula) -> bool:
        """Adiciona matrícula à turma respeitando capacidade (RN05)."""
        return turma.adicionar_matricula(matricula)

    def remover_matricula(self, turma, matricula) -> None:
        """Remove matrícula da turma."""
        turma.remover_matricula(matricula)

    # --- Matérias ---

    def adicionar_materia(self, turma, materia) -> None:
        """Associa matéria à turma."""
        turma.adicionar_materia(materia)

    def remover_materia(self, turma, materia) -> None:
        """Remove associação de matéria da turma."""
        turma.remover_materia(materia)

    def listar_materias(self, turma) -> list:
        """Lista matérias da turma."""
        return turma.materias
