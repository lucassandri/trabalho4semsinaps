# controller/serie_controller.py
# Controller de Serie - opera sobre objetos Serie e o cache

from cache.cache_manager import CacheManager


class SerieController:
    """Gerencia operações sobre Serie: busca, listagem e turmas compostas."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Consultas ---

    def buscar(self, codigo: str):
        """Busca série pelo código."""
        return self._cache.buscar_serie(codigo)

    def listar(self) -> list:
        """Lista todas as séries cadastradas."""
        return self._cache.listar_series()

    # --- Turmas compostas ---

    def listar_turmas(self, serie) -> list:
        """Lista turmas de uma série (Composição)."""
        return serie.listar_turmas()

    def adicionar_turma(self, serie, turma) -> None:
        """Adiciona turma à série (Composição)."""
        serie.adicionar_turma(turma)

    def remover_turma(self, serie, turma) -> None:
        """Remove turma da série (Composição)."""
        serie.remover_turma(turma)
