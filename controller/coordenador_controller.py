# controller/coordenador_controller.py
# Controller de Coordenador - delega RF04 ao objeto Coordenador

from cache.cache_manager import CacheManager


class CoordenadorController:
    """Gerencia operações do Coordenador: séries, turmas, matérias e atribuições (RF04)."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Séries (RF04) ---

    def cadastrar_serie(self, coordenador, dados: dict):
        """Cadastra nova série via Coordenador (RF04)."""
        return coordenador.cadastrar_serie(dados)

    def editar_serie(self, coordenador, codigo: str, dados: dict) -> bool:
        """Edita série existente via Coordenador (RF04)."""
        return coordenador.editar_serie(codigo, dados)

    def buscar_serie(self, codigo: str):
        """Busca série pelo código."""
        return self._cache.buscar_serie(codigo)

    def listar_series(self) -> list:
        """Lista todas as séries cadastradas."""
        return self._cache.listar_series()

    # --- Turmas (RF04) ---

    def cadastrar_turma(self, coordenador, dados: dict):
        """Cadastra nova turma via Coordenador (RF04, RN05 - capacidade obrigatória)."""
        return coordenador.cadastrar_turma(dados)

    def editar_turma(self, coordenador, codigo: str, dados: dict) -> bool:
        """Edita turma existente via Coordenador (RF04)."""
        return coordenador.editar_turma(codigo, dados)

    def buscar_turma(self, codigo: str):
        """Busca turma pelo código."""
        return self._cache.buscar_turma(codigo)

    def listar_turmas(self) -> list:
        """Lista todas as turmas cadastradas."""
        return self._cache.listar_turmas()

    # --- Matérias (RF04) ---

    def cadastrar_materia(self, coordenador, dados: dict):
        """Cadastra nova matéria via Coordenador (RF04)."""
        return coordenador.cadastrar_materia(dados)

    def editar_materia(self, coordenador, codigo: str, dados: dict) -> bool:
        """Edita matéria existente via Coordenador (RF04)."""
        return coordenador.editar_materia(codigo, dados)

    def buscar_materia(self, codigo: str):
        """Busca matéria pelo código."""
        return self._cache.buscar_materia(codigo)

    def listar_materias(self) -> list:
        """Lista todas as matérias cadastradas."""
        return self._cache.listar_materias()

    # --- Atribuição (RF04) ---

    def atribuir_professor_materia(self, coordenador, mat_prof: str,
                                   cod_materia: str, cod_turma: str) -> bool:
        """Atribui professor a matéria/turma via Coordenador (RF04)."""
        professor = self._cache.buscar_professor(mat_prof)
        materia = self._cache.buscar_materia(cod_materia)
        turma = self._cache.buscar_turma(cod_turma)
        if not professor or not materia or not turma:
            return False
        return coordenador.atribuir_professor_materia(professor, materia, turma)
