# controller/secretaria_controller.py
# Controller de Secretaria - responsável pela lógica de persistência e orquestração (RF01-RF03, RF10, RF11)
# O Model (Secretaria) cria/modifica objetos de domínio; este controller gerencia o cache.

from cache.cache_manager import CacheManager


class SecretariaController:
    """Gerencia operações da Secretaria: alunos, funcionários, matrículas, relatórios."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Alunos (RF01) ---

    def cadastrar_aluno(self, secretaria, dados: dict) -> bool:
        """Verifica duplicidade, cria Aluno via Secretaria e persiste (RF01)."""
        if self._cache.buscar_aluno(dados.get("cpf", "")) is not None:
            return False
        aluno = secretaria.criar_aluno(dados)
        self._cache.adicionar_aluno(aluno)
        return True

    def editar_aluno(self, secretaria, cpf: str, dados: dict) -> bool:
        """Busca Aluno no cache, delega edição à Secretaria e persiste (RF01)."""
        aluno = self._cache.buscar_aluno(cpf)
        if aluno is None:
            return False
        secretaria.atualizar_aluno(aluno, dados)
        self._cache.atualizar_aluno(aluno)
        return True

    def consultar_aluno(self, cpf: str):
        """Busca aluno pelo CPF (RF01)."""
        return self._cache.buscar_aluno(cpf)

    def listar_alunos(self) -> list:
        """Lista todos os alunos cadastrados."""
        return self._cache.listar_alunos()

    # --- Funcionários (RF03) ---

    def cadastrar_funcionario(self, secretaria, dados: dict) -> bool:
        """Verifica duplicidade, cria Funcionário via Secretaria e persiste (RF03)."""
        matricula = dados.get("matricula_funcionario", "")
        if (self._cache.buscar_professor(matricula)
                or self._cache.buscar_secretaria(matricula)
                or self._cache.buscar_coordenador(matricula)):
            return False
        func = secretaria.criar_funcionario(dados)
        # Persiste no compartimento correto conforme tipo criado
        from model.professor import Professor
        from model.coordenador import Coordenador
        if isinstance(func, Professor):
            self._cache.adicionar_professor(func)
        elif isinstance(func, Coordenador):
            self._cache.adicionar_coordenador(func)
        else:
            self._cache.adicionar_secretaria(func)
        return True

    def editar_funcionario(self, secretaria, matricula: str, dados: dict) -> bool:
        """Busca Funcionário no cache, delega edição à Secretaria e persiste (RF03)."""
        func = (self._cache.buscar_professor(matricula)
                or self._cache.buscar_secretaria(matricula)
                or self._cache.buscar_coordenador(matricula))
        if func is None:
            return False
        secretaria.atualizar_funcionario(func, dados)
        return True

    def consultar_funcionario(self, matricula: str):
        """Busca funcionário pela matrícula (RF03)."""
        return (self._cache.buscar_professor(matricula)
                or self._cache.buscar_secretaria(matricula)
                or self._cache.buscar_coordenador(matricula))

    def listar_professores(self) -> list:
        """Lista todos os professores cadastrados (RF03)."""
        return self._cache.listar_professores()

    # --- Matrículas (RF02) ---

    def efetuar_matricula(self, secretaria, cpf_aluno: str, cod_turma: str):
        """Efetua matrícula: verifica dados, delega criação à Secretaria e persiste (RF02, RN05)."""
        aluno = self._cache.buscar_aluno(cpf_aluno)
        turma = self._cache.buscar_turma(cod_turma)
        if not aluno or not turma:
            return None
        mat = secretaria.efetuar_matricula(aluno, turma)
        if mat:
            self._cache.adicionar_matricula(mat)
        return mat

    def cancelar_matricula(self, secretaria, cod_matricula: str) -> bool:
        """Busca matrícula e delega cancelamento à Secretaria (RF02)."""
        matricula = self._cache.buscar_matricula(cod_matricula)
        if not matricula:
            return False
        secretaria.cancelar_matricula(matricula)
        return True

    def transferir_matricula(self, secretaria, cod_matricula: str, cod_turma_dest: str) -> bool:
        """Busca matrícula e turma, delega transferência à Secretaria (RF02, RN05)."""
        matricula = self._cache.buscar_matricula(cod_matricula)
        turma = self._cache.buscar_turma(cod_turma_dest)
        if not matricula or not turma:
            return False
        return secretaria.transferir_matricula(matricula, turma)

    # --- Histórico (RF10) ---

    def emitir_historico(self, secretaria, cpf_aluno: str):
        """Busca aluno e delega emissão do histórico à Secretaria (RF10)."""
        aluno = self._cache.buscar_aluno(cpf_aluno)
        if not aluno:
            return None
        return secretaria.emitir_historico(aluno)

    # --- Relatórios (RF11) ---

    def gerar_relatorio_turma(self, secretaria, cod_turma: str) -> list:
        """Busca turma e alunos no cache, delega geração do relatório à Secretaria (RF11)."""
        turma = self._cache.buscar_turma(cod_turma)
        if not turma:
            return []
        alunos = self._cache.listar_alunos()
        return secretaria.gerar_relatorio_turma(turma, alunos)

    def gerar_relatorio_professores(self, secretaria, cod_serie: str) -> list:
        """Busca série e professores no cache, delega geração do relatório à Secretaria (RF11)."""
        serie = self._cache.buscar_serie(cod_serie)
        if not serie:
            return []
        professores = self._cache.listar_professores()
        return secretaria.gerar_relatorio_professores(serie, professores)
