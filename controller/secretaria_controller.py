# controller/secretaria_controller.py
# Controller de Secretaria - delega RF01, RF02, RF03, RF10, RF11 ao objeto Secretaria

from cache.cache_manager import CacheManager


class SecretariaController:
    """Gerencia operações da Secretaria: alunos, funcionários, matrículas, relatórios."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Alunos (RF01) ---

    def cadastrar_aluno(self, secretaria, dados: dict) -> bool:
        """Cadastra novo aluno via Secretaria (RF01)."""
        return secretaria.cadastrar_aluno(dados)

    def editar_aluno(self, secretaria, cpf: str, dados: dict) -> bool:
        """Edita dados de aluno via Secretaria (RF01)."""
        return secretaria.editar_aluno(cpf, dados)

    def consultar_aluno(self, cpf: str):
        """Consulta aluno pelo CPF (RF01)."""
        return self._cache.buscar_aluno(cpf)

    def listar_alunos(self) -> list:
        """Lista todos os alunos cadastrados."""
        return self._cache.listar_alunos()

    # --- Funcionários (RF03) ---

    def cadastrar_funcionario(self, secretaria, dados: dict) -> bool:
        """Cadastra novo funcionário via Secretaria (RF03)."""
        return secretaria.cadastrar_funcionario(dados)

    def editar_funcionario(self, secretaria, matricula: str, dados: dict) -> bool:
        """Edita dados de funcionário via Secretaria (RF03)."""
        return secretaria.editar_funcionario(matricula, dados)

    def consultar_funcionario(self, matricula: str):
        """Consulta funcionário pela matrícula (RF03)."""
        return (self._cache.buscar_professor(matricula)
                or self._cache.buscar_secretaria(matricula)
                or self._cache.buscar_coordenador(matricula))

    # --- Matrículas (RF02) ---

    def efetuar_matricula(self, secretaria, cpf_aluno: str, cod_turma: str):
        """Efetua matrícula de aluno em turma via Secretaria (RF02, RN05)."""
        aluno = self._cache.buscar_aluno(cpf_aluno)
        turma = self._cache.buscar_turma(cod_turma)
        if not aluno or not turma:
            return None
        return secretaria.efetuar_matricula(aluno, turma)

    def cancelar_matricula(self, secretaria, cod_matricula: str) -> bool:
        """Cancela matrícula via Secretaria (RF02)."""
        matricula = self._cache.buscar_matricula(cod_matricula)
        if not matricula:
            return False
        return secretaria.cancelar_matricula(matricula)

    def transferir_matricula(self, secretaria, cod_matricula: str, cod_turma_dest: str) -> bool:
        """Transfere matrícula para outra turma via Secretaria (RF02, RN05)."""
        matricula = self._cache.buscar_matricula(cod_matricula)
        turma = self._cache.buscar_turma(cod_turma_dest)
        if not matricula or not turma:
            return False
        return secretaria.transferir_matricula(matricula, turma)

    # --- Histórico (RF10) ---

    def emitir_historico(self, secretaria, cpf_aluno: str):
        """Emite histórico escolar completo do aluno via Secretaria (RF10)."""
        aluno = self._cache.buscar_aluno(cpf_aluno)
        if not aluno:
            return None
        return secretaria.emitir_historico(aluno)

    # --- Relatórios (RF11) ---

    def gerar_relatorio_turma(self, secretaria, cod_turma: str) -> list:
        """Gera relatório de alunos por turma via Secretaria (RF11)."""
        turma = self._cache.buscar_turma(cod_turma)
        if not turma:
            return []
        return secretaria.gerar_relatorio_turma(turma)

    def gerar_relatorio_professores(self, secretaria, cod_serie: str) -> list:
        """Gera relatório de professores por série via Secretaria (RF11)."""
        serie = self._cache.buscar_serie(cod_serie)
        if not serie:
            return []
        return secretaria.gerar_relatorio_professores(serie)
