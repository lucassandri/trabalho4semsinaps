# controller/professor_controller.py
# Controller do ator Professor - apenas operações que o Professor executa (RF05, RF06)
# Listagem/busca de professores: RF03 (Secretaria) → SecretariaController
#                                 RF04 (Coordenador) → CoordenadorController

from cache.cache_manager import CacheManager


class ProfessorController:
    """Operações do ator Professor: registrar notas (RF05) e frequências (RF06)."""

    def __init__(self):
        self._cache = CacheManager()

    def registrar_nota(self, professor, cod_matricula: str, cod_materia: str,
                       bimestre: int, valor: float) -> bool:
        """Registra nota bimestral via Professor (RF05, RN06)."""
        matricula = self._cache.buscar_matricula(cod_matricula)
        materia = self._cache.buscar_materia(cod_materia)
        if not matricula or not materia:
            return False
        return professor.registrar_nota(matricula, materia, bimestre, valor)

    def registrar_frequencia(self, professor, cod_matricula: str, cod_materia: str,
                             data_aula, presente: bool) -> bool:
        """Registra frequência de aula via Professor (RF06)."""
        matricula = self._cache.buscar_matricula(cod_matricula)
        materia = self._cache.buscar_materia(cod_materia)
        if not matricula or not materia:
            return False
        return professor.registrar_frequencia(matricula, materia, data_aula, presente)

    def editar_frequencia(self, professor, cod_matricula: str, cod_materia: str,
                          data_aula, presente: bool) -> bool:
        """Edita frequência de dia anterior via Professor (RF06)."""
        matricula = self._cache.buscar_matricula(cod_matricula)
        materia = self._cache.buscar_materia(cod_materia)
        if not matricula or not materia:
            return False
        return professor.editar_frequencia(matricula, materia, data_aula, presente)
