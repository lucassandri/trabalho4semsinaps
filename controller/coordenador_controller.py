# controller/coordenador_controller.py
# Controller de Coordenador - responsável pela lógica de persistência e orquestração (RF04)
# O Model (Coordenador) cria/modifica objetos de domínio; este controller gerencia o cache.

from cache.cache_manager import CacheManager


class CoordenadorController:
    """Gerencia operações do Coordenador: séries, turmas, matérias e atribuições (RF04)."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Séries (RF04) ---

    def cadastrar_serie(self, coordenador, dados: dict):
        """Verifica duplicidade, cria Serie via Coordenador e persiste (RF04)."""
        if self._cache.buscar_serie(dados.get("codigo", "")) is not None:
            return None
        serie = coordenador.criar_serie(dados)
        self._cache.adicionar_serie(serie)
        return serie

    def editar_serie(self, coordenador, codigo: str, dados: dict) -> bool:
        """Busca Serie no cache, delega edição ao Coordenador (RF04)."""
        serie = self._cache.buscar_serie(codigo)
        if serie is None:
            return False
        coordenador.atualizar_serie(serie, dados)
        return True

    def buscar_serie(self, codigo: str):
        """Busca série pelo código."""
        return self._cache.buscar_serie(codigo)

    def listar_series(self) -> list:
        """Lista todas as séries cadastradas."""
        return self._cache.listar_series()

    # --- Turmas (RF04) ---

    def cadastrar_turma(self, coordenador, dados: dict):
        """Busca Série, verifica dados, cria Turma via Coordenador e persiste (RF04, RN05)."""
        if "capacidade_maxima" not in dados:
            return None
        serie = self._cache.buscar_serie(dados.get("codigo_serie", ""))
        if serie is None:
            return None
        turma = coordenador.criar_turma(dados, serie)
        if turma:
            self._cache.adicionar_turma(turma)
        return turma

    def editar_turma(self, coordenador, codigo: str, dados: dict) -> bool:
        """Busca Turma no cache, delega edição ao Coordenador (RF04)."""
        turma = self._cache.buscar_turma(codigo)
        if turma is None:
            return False
        coordenador.atualizar_turma(turma, dados)
        return True

    def buscar_turma(self, codigo: str):
        """Busca turma pelo código."""
        return self._cache.buscar_turma(codigo)

    def listar_turmas(self) -> list:
        """Lista todas as turmas cadastradas."""
        return self._cache.listar_turmas()

    # --- Matérias (RF04) ---

    def cadastrar_materia(self, coordenador, dados: dict):
        """Verifica duplicidade, cria Materia via Coordenador e persiste (RF04)."""
        if self._cache.buscar_materia(dados.get("codigo", "")) is not None:
            return None
        materia = coordenador.criar_materia(dados)
        self._cache.adicionar_materia(materia)
        return materia

    def editar_materia(self, coordenador, codigo: str, dados: dict) -> bool:
        """Busca Materia no cache, delega edição ao Coordenador (RF04)."""
        materia = self._cache.buscar_materia(codigo)
        if materia is None:
            return False
        coordenador.atualizar_materia(materia, dados)
        return True

    def buscar_materia(self, codigo: str):
        """Busca matéria pelo código."""
        return self._cache.buscar_materia(codigo)

    def listar_materias(self) -> list:
        """Lista todas as matérias cadastradas."""
        return self._cache.listar_materias()

    # --- Atribuição (RF04) ---

    def atribuir_professor_materia(self, coordenador, mat_prof: str,
                                   cod_materia: str, cod_turma: str) -> bool:
        """Busca objetos no cache e delega atribuição ao Coordenador (RF04)."""
        professor = self._cache.buscar_professor(mat_prof)
        materia = self._cache.buscar_materia(cod_materia)
        turma = self._cache.buscar_turma(cod_turma)
        if not professor or not materia or not turma:
            return False
        return coordenador.atribuir_professor_materia(professor, materia, turma)
