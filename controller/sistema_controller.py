# controller/sistema_controller.py
# Controller unificado que intermedia View e Model
# Cada método delega para o objeto de domínio correspondente

from cache.cache_manager import CacheManager


class SistemaController:
    """Controller central que orquestra operações entre View e Model."""

    def __init__(self):
        self._cache = CacheManager()
        self._usuario_logado = None
        self._pessoa_logada = None

    @property
    def usuario_logado(self):
        return self._usuario_logado

    @property
    def pessoa_logada(self):
        return self._pessoa_logada

    # --- Autenticação (RF12) ---

    def autenticar(self, login: str, senha: str) -> bool:
        """Autentica usuário no sistema (RF12).
        Returns:
            True se autenticou, False se credenciais inválidas.
        """
        usuario = self._cache.buscar_usuario(login)
        if usuario and usuario.autenticar(login, senha):
            self._usuario_logado = usuario
            # Busca a pessoa associada ao login
            self._pessoa_logada = self._buscar_pessoa_por_login(login)
            return True
        return False

    def _buscar_pessoa_por_login(self, login: str):
        """Busca a Pessoa associada ao login no cache."""
        # Busca em todas as listas de pessoas
        for aluno in self._cache.listar_alunos():
            if aluno.usuario and aluno.usuario.login == login:
                return aluno
        for prof in self._cache.listar_professores():
            if prof.usuario and prof.usuario.login == login:
                return prof
        for sec in self._cache.listar_secretarias():
            if sec.usuario and sec.usuario.login == login:
                return sec
        for coord in self._cache.listar_coordenadores():
            if coord.usuario and coord.usuario.login == login:
                return coord
        return None

    def obter_perfil(self) -> str:
        """Retorna o perfil do usuário logado."""
        if self._usuario_logado:
            return self._usuario_logado.perfil
        return ""

    # --- Alunos (RF01) - delega para Secretaria ---

    def cadastrar_aluno(self, dados: dict) -> bool:
        """Cadastra aluno via Secretaria logada (RF01)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            return self._pessoa_logada.cadastrar_aluno(dados)
        return False

    def editar_aluno(self, cpf: str, dados: dict) -> bool:
        """Edita aluno via Secretaria logada (RF01)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            return self._pessoa_logada.editar_aluno(cpf, dados)
        return False

    def consultar_aluno(self, cpf: str):
        """Consulta aluno via Secretaria logada (RF01)."""
        return self._cache.buscar_aluno(cpf)

    def listar_alunos(self) -> list:
        """Lista todos os alunos."""
        return self._cache.listar_alunos()

    # --- Funcionários (RF03) - delega para Secretaria ---

    def cadastrar_funcionario(self, dados: dict) -> bool:
        """Cadastra funcionário via Secretaria logada (RF03)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            return self._pessoa_logada.cadastrar_funcionario(dados)
        return False

    def editar_funcionario(self, matricula: str, dados: dict) -> bool:
        """Edita funcionário via Secretaria logada (RF03)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            return self._pessoa_logada.editar_funcionario(matricula, dados)
        return False

    def consultar_funcionario(self, matricula: str):
        """Consulta funcionário (RF03)."""
        return (self._cache.buscar_professor(matricula)
                or self._cache.buscar_secretaria(matricula)
                or self._cache.buscar_coordenador(matricula))

    def listar_professores(self) -> list:
        return self._cache.listar_professores()

    # --- Séries, Turmas, Matérias (RF04) - delega para Coordenador ---

    def cadastrar_serie(self, dados: dict):
        """Cadastra série via Coordenador (RF04)."""
        if isinstance(self._pessoa_logada, self._get_class("Coordenador")):
            return self._pessoa_logada.cadastrar_serie(dados)
        return None

    def cadastrar_turma(self, dados: dict):
        """Cadastra turma com capacidade_maxima via Coordenador (RF04, RN05)."""
        if isinstance(self._pessoa_logada, self._get_class("Coordenador")):
            return self._pessoa_logada.cadastrar_turma(dados)
        return None

    def cadastrar_materia(self, dados: dict):
        """Cadastra matéria via Coordenador (RF04)."""
        if isinstance(self._pessoa_logada, self._get_class("Coordenador")):
            return self._pessoa_logada.cadastrar_materia(dados)
        return None

    def atribuir_professor_materia(self, mat_prof: str, cod_materia: str, cod_turma: str) -> bool:
        """Atribui professor a matéria/turma via Coordenador (RF04)."""
        if isinstance(self._pessoa_logada, self._get_class("Coordenador")):
            prof = self._cache.buscar_professor(mat_prof)
            materia = self._cache.buscar_materia(cod_materia)
            turma = self._cache.buscar_turma(cod_turma)
            if prof and materia and turma:
                return self._pessoa_logada.atribuir_professor_materia(prof, materia, turma)
        return False

    def listar_series(self) -> list:
        return self._cache.listar_series()

    def listar_turmas(self) -> list:
        return self._cache.listar_turmas()

    def listar_materias(self) -> list:
        return self._cache.listar_materias()

    # --- Matrículas (RF02) - delega para Secretaria ---

    def efetuar_matricula(self, cpf_aluno: str, cod_turma: str):
        """Efetua matrícula via Secretaria (RF02, RN05)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            aluno = self._cache.buscar_aluno(cpf_aluno)
            turma = self._cache.buscar_turma(cod_turma)
            if aluno and turma:
                return self._pessoa_logada.efetuar_matricula(aluno, turma)
        return None

    def cancelar_matricula(self, cod_matricula: str) -> bool:
        """Cancela matrícula via Secretaria (RF02)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            mat = self._cache.buscar_matricula(cod_matricula)
            if mat:
                return self._pessoa_logada.cancelar_matricula(mat)
        return False

    def transferir_matricula(self, cod_matricula: str, cod_turma_dest: str) -> bool:
        """Transfere matrícula via Secretaria (RF02, RN05)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            mat = self._cache.buscar_matricula(cod_matricula)
            turma = self._cache.buscar_turma(cod_turma_dest)
            if mat and turma:
                return self._pessoa_logada.transferir_matricula(mat, turma)
        return False

    def listar_matriculas(self) -> list:
        return self._cache.listar_matriculas()

    # --- Notas (RF05) - delega para Professor ---

    def registrar_nota(self, cod_matricula: str, cod_materia: str,
                       bimestre: int, valor: float) -> bool:
        """Registra nota via Professor (RF05, RN06)."""
        if isinstance(self._pessoa_logada, self._get_class("Professor")):
            mat = self._cache.buscar_matricula(cod_matricula)
            materia = self._cache.buscar_materia(cod_materia)
            if mat and materia:
                return self._pessoa_logada.registrar_nota(mat, materia, bimestre, valor)
        return False

    # --- Frequência (RF06) - delega para Professor ---

    def registrar_frequencia(self, cod_matricula: str, cod_materia: str,
                             data_aula, presente: bool) -> bool:
        """Registra frequência via Professor (RF06)."""
        if isinstance(self._pessoa_logada, self._get_class("Professor")):
            mat = self._cache.buscar_matricula(cod_matricula)
            materia = self._cache.buscar_materia(cod_materia)
            if mat and materia:
                return self._pessoa_logada.registrar_frequencia(
                    mat, materia, data_aula, presente
                )
        return False

    def editar_frequencia(self, cod_matricula: str, cod_materia: str,
                          data_aula, presente: bool) -> bool:
        """Edita frequência de dia anterior via Professor (RF06)."""
        if isinstance(self._pessoa_logada, self._get_class("Professor")):
            mat = self._cache.buscar_matricula(cod_matricula)
            materia = self._cache.buscar_materia(cod_materia)
            if mat and materia:
                return self._pessoa_logada.editar_frequencia(
                    mat, materia, data_aula, presente
                )
        return False

    # --- Boletim (RF07, RF08, RF09) ---

    def gerar_boletim(self, cod_matricula: str):
        """Gera boletim calculando média e situação (RF07, RF08)."""
        mat = self._cache.buscar_matricula(cod_matricula)
        if mat and mat.boletim:
            boletim = mat.boletim
            # RF07: calcula média final (RN04)
            boletim.calcular_media_final()
            # Calcula frequência percentual
            boletim.calcular_frequencia_percentual(mat.frequencias)
            # RF07: determina situação (RN01, RN02, RN03)
            boletim.determinar_situacao()
            return boletim
        return None

    def consultar_boletim_aluno(self, cod_matricula: str):
        """Consulta boletim pelo aluno (RF09)."""
        if isinstance(self._pessoa_logada, self._get_class("Aluno")):
            mat = self._cache.buscar_matricula(cod_matricula)
            if mat:
                return self._pessoa_logada.consultar_boletim(mat)
        return None

    # --- Histórico (RF09, RF10) ---

    def emitir_historico(self, cpf_aluno: str):
        """Emite histórico via Secretaria (RF10)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            aluno = self._cache.buscar_aluno(cpf_aluno)
            if aluno:
                return self._pessoa_logada.emitir_historico(aluno)
        return None

    def consultar_historico_aluno(self):
        """Consulta histórico pelo aluno (RF09)."""
        if isinstance(self._pessoa_logada, self._get_class("Aluno")):
            return self._pessoa_logada.consultar_historico()
        return None

    # --- Relatórios (RF11) ---

    def gerar_relatorio_turma(self, cod_turma: str) -> list:
        """Gera relatório de alunos por turma (RF11)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            turma = self._cache.buscar_turma(cod_turma)
            if turma:
                return self._pessoa_logada.gerar_relatorio_turma(turma)
        return []

    def gerar_relatorio_professores(self, cod_serie: str) -> list:
        """Gera relatório de professores por série/matéria (RF11)."""
        if isinstance(self._pessoa_logada, self._get_class("Secretaria")):
            serie = self._cache.buscar_serie(cod_serie)
            if serie:
                return self._pessoa_logada.gerar_relatorio_professores(serie)
        return []

    # --- Utilitário ---

    def _get_class(self, nome: str):
        """Retorna a classe do model pelo nome (evita import circular)."""
        import model
        return getattr(model, nome)
