# controller/sistema_controller.py
# Controller de sessão - responsável apenas por autenticação (RF12) e estado do usuário logado

from cache.cache_manager import CacheManager


class SistemaController:
    """Gerencia autenticação e sessão do usuário logado (RF12)."""

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

    def autenticar(self, login: str, senha: str) -> bool:
        """Autentica usuário no sistema (RF12).
        Returns:
            True se credenciais válidas, False caso contrário.
        """
        usuario = self._cache.buscar_usuario(login)
        if usuario and usuario.autenticar(login, senha):
            self._usuario_logado = usuario
            self._pessoa_logada = self._buscar_pessoa_por_login(login)
            return True
        return False

    def obter_perfil(self) -> str:
        """Retorna o perfil do usuário logado."""
        return self._usuario_logado.perfil if self._usuario_logado else ""

    def logout(self):
        """Encerra a sessão do usuário."""
        self._usuario_logado = None
        self._pessoa_logada = None

    def _buscar_pessoa_por_login(self, login: str):
        """Busca a Pessoa associada ao login no cache."""
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
