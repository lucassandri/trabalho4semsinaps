# controller/matricula_controller.py
# Controller de Matricula - opera sobre objetos Matricula e o cache

from cache.cache_manager import CacheManager


class MatriculaController:
    """Gerencia operações sobre Matricula: cancelamento, transferência e boletim."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Consultas ---

    def buscar(self, codigo: str):
        """Busca matrícula pelo código."""
        return self._cache.buscar_matricula(codigo)

    def listar(self) -> list:
        """Lista todas as matrículas."""
        return self._cache.listar_matriculas()

    # --- Operações (RF02) ---

    def cancelar(self, matricula) -> None:
        """Cancela a matrícula (RF02)."""
        matricula.cancelar()

    def transferir(self, matricula, turma_destino) -> None:
        """Transfere matrícula para turma destino (RF02)."""
        matricula.transferir(turma_destino)

    # --- Boletim (Composição) ---

    def criar_boletim(self, matricula):
        """Cria e retorna o boletim vinculado à matrícula (Composição)."""
        return matricula.criar_boletim()

    def obter_boletim(self, matricula):
        """Retorna o boletim da matrícula."""
        return matricula.boletim

    # --- Frequências (Composição) ---

    def adicionar_frequencia(self, matricula, frequencia) -> None:
        """Adiciona registro de frequência à matrícula (Composição)."""
        matricula.adicionar_frequencia(frequencia)

    def listar_frequencias(self, matricula) -> list:
        """Lista frequências da matrícula."""
        return matricula.frequencias
