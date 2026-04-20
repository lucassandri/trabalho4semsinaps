# controller/aluno_controller.py
# Controller do ator Aluno - apenas operações que o Aluno executa (RF09)
# Busca/listagem de alunos é RF01 (Secretaria) → SecretariaController

from cache.cache_manager import CacheManager


class AlunoController:
    """Operações do ator Aluno: consulta de boletim e histórico (RF09)."""

    def __init__(self):
        self._cache = CacheManager()

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
        """Lista matrículas do aluno (RF09)."""
        return aluno.matriculas

    def listar_historicos(self, aluno) -> list:
        """Lista históricos escolares do aluno (RF09)."""
        return aluno.historicos
