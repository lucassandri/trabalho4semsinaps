# controller/materia_controller.py
# Controller de Materia - opera sobre objetos Materia e o cache

from cache.cache_manager import CacheManager


class MateriaController:
    """Gerencia operações sobre Materia: busca e listagem."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Consultas ---

    def buscar(self, codigo: str):
        """Busca matéria pelo código."""
        return self._cache.buscar_materia(codigo)

    def listar(self) -> list:
        """Lista todas as matérias cadastradas."""
        return self._cache.listar_materias()
