# controller/aluno_controller.py
# Controller de Aluno - delega RF09 ao objeto Aluno

from cache.cache_manager import CacheManager


class AlunoController:
    """Gerencia operações do Aluno: consulta de boletim e histórico (RF09)."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Consultas (RF09) ---

    def consultar_boletim(self, aluno, cod_matricula: str):
        """Consulta boletim de uma matrícula via Aluno (RF09)."""
        matricula = self._cache.buscar_matricula(cod_matricula)
        if not matricula:
            return None
        return aluno.consultar_boletim(matricula)

    def consultar_historico(self, aluno):
        """Consulta histórico escolar via Aluno (RF09)."""
        return aluno.consultar_historico()

    def listar_matriculas(self, aluno) -> list:
        """Lista matrículas do aluno."""
        return aluno.matriculas

    def listar_historicos(self, aluno) -> list:
        """Lista históricos escolares do aluno."""
        return aluno.historicos

    # --- Busca ---

    def buscar_aluno(self, cpf: str):
        """Busca aluno pelo CPF."""
        return self._cache.buscar_aluno(cpf)

    def listar_alunos(self) -> list:
        """Lista todos os alunos."""
        return self._cache.listar_alunos()
