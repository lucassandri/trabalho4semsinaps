# cache/cache_manager.py
# Gerenciador de cache em memória (Singleton)
# Armazena objetos de cada classe do domínio em dicionários

class CacheManager:
    """Singleton que gerencia o cache em memória de todas as entidades."""

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        """Inicializa os dicionários de cache."""
        self._alunos: dict = {}          # chave: cpf
        self._professores: dict = {}     # chave: matricula_funcionario
        self._secretarias: dict = {}     # chave: matricula_funcionario
        self._coordenadores: dict = {}   # chave: matricula_funcionario
        self._usuarios: dict = {}        # chave: login
        self._series: dict = {}          # chave: codigo
        self._turmas: dict = {}          # chave: codigo
        self._materias: dict = {}        # chave: codigo
        self._matriculas: dict = {}      # chave: codigo

    # --- Alunos ---
    def adicionar_aluno(self, aluno):
        self._alunos[aluno.cpf] = aluno

    def remover_aluno(self, cpf: str):
        self._alunos.pop(cpf, None)

    def buscar_aluno(self, cpf: str):
        return self._alunos.get(cpf)

    def listar_alunos(self) -> list:
        return list(self._alunos.values())

    def atualizar_aluno(self, aluno):
        self._alunos[aluno.cpf] = aluno

    # --- Professores ---
    def adicionar_professor(self, professor):
        self._professores[professor.matricula_funcionario] = professor

    def remover_professor(self, matricula: str):
        self._professores.pop(matricula, None)

    def buscar_professor(self, matricula: str):
        return self._professores.get(matricula)

    def listar_professores(self) -> list:
        return list(self._professores.values())

    def atualizar_professor(self, professor):
        self._professores[professor.matricula_funcionario] = professor

    # --- Secretarias ---
    def adicionar_secretaria(self, secretaria):
        self._secretarias[secretaria.matricula_funcionario] = secretaria

    def remover_secretaria(self, matricula: str):
        self._secretarias.pop(matricula, None)

    def buscar_secretaria(self, matricula: str):
        return self._secretarias.get(matricula)

    def listar_secretarias(self) -> list:
        return list(self._secretarias.values())

    # --- Coordenadores ---
    def adicionar_coordenador(self, coordenador):
        self._coordenadores[coordenador.matricula_funcionario] = coordenador

    def buscar_coordenador(self, matricula: str):
        return self._coordenadores.get(matricula)

    def listar_coordenadores(self) -> list:
        return list(self._coordenadores.values())

    # --- Usuarios ---
    def adicionar_usuario(self, usuario):
        self._usuarios[usuario.login] = usuario

    def buscar_usuario(self, login: str):
        return self._usuarios.get(login)

    def listar_usuarios(self) -> list:
        return list(self._usuarios.values())

    # --- Series ---
    def adicionar_serie(self, serie):
        self._series[serie.codigo] = serie

    def remover_serie(self, codigo: str):
        self._series.pop(codigo, None)

    def buscar_serie(self, codigo: str):
        return self._series.get(codigo)

    def listar_series(self) -> list:
        return list(self._series.values())

    # --- Turmas ---
    def adicionar_turma(self, turma):
        self._turmas[turma.codigo] = turma

    def remover_turma(self, codigo: str):
        self._turmas.pop(codigo, None)

    def buscar_turma(self, codigo: str):
        return self._turmas.get(codigo)

    def listar_turmas(self) -> list:
        return list(self._turmas.values())

    # --- Materias ---
    def adicionar_materia(self, materia):
        self._materias[materia.codigo] = materia

    def remover_materia(self, codigo: str):
        self._materias.pop(codigo, None)

    def buscar_materia(self, codigo: str):
        return self._materias.get(codigo)

    def listar_materias(self) -> list:
        return list(self._materias.values())

    # --- Matriculas ---
    def adicionar_matricula(self, matricula):
        self._matriculas[matricula.codigo] = matricula

    def remover_matricula(self, codigo: str):
        self._matriculas.pop(codigo, None)

    def buscar_matricula(self, codigo: str):
        return self._matriculas.get(codigo)

    def listar_matriculas(self) -> list:
        return list(self._matriculas.values())

    # --- Utilitários ---
    def limpar_cache(self):
        """Limpa todo o cache do sistema."""
        self._inicializar()

    def contar_entidades(self) -> dict:
        """Retorna contagem de entidades por tipo."""
        return {
            "alunos": len(self._alunos),
            "professores": len(self._professores),
            "secretarias": len(self._secretarias),
            "coordenadores": len(self._coordenadores),
            "usuarios": len(self._usuarios),
            "series": len(self._series),
            "turmas": len(self._turmas),
            "materias": len(self._materias),
            "matriculas": len(self._matriculas)
        }
