# controller/professor_controller.py
# Controller de Professor - delega RF05 e RF06 ao objeto Professor

from cache.cache_manager import CacheManager


class ProfessorController:
    """Gerencia operações do Professor: notas (RF05) e frequências (RF06)."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Notas (RF05) ---

    def registrar_nota(self, professor, cod_matricula: str, cod_materia: str,
                       bimestre: int, valor: float) -> bool:
        """Registra nota bimestral via Professor (RF05, RN06)."""
        matricula = self._cache.buscar_matricula(cod_matricula)
        materia = self._cache.buscar_materia(cod_materia)
        if not matricula or not materia:
            return False
        return professor.registrar_nota(matricula, materia, bimestre, valor)

    # --- Frequência (RF06) ---

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

    # --- Consultas ---

    def listar_professores(self) -> list:
        """Lista todos os professores cadastrados."""
        return self._cache.listar_professores()

    def buscar_professor(self, matricula_funcionario: str):
        """Busca professor pela matrícula funcional."""
        return self._cache.buscar_professor(matricula_funcionario)
