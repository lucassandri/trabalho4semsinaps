# controller/usuario_controller.py
# Controller de Usuario - delega RF12 ao objeto Usuario

from cache.cache_manager import CacheManager


class UsuarioController:
    """Gerencia operações de Usuario: autenticação e manutenção de conta (RF12)."""

    def __init__(self):
        self._cache = CacheManager()

    # --- Autenticação (RF12) ---

    def autenticar(self, login: str, senha: str):
        """Autentica usuário no sistema (RF12).
        Returns:
            Objeto Usuario se autenticou com sucesso, None caso contrário.
        """
        usuario = self._cache.buscar_usuario(login)
        if usuario and usuario.autenticar(login, senha):
            return usuario
        return None

    def alterar_senha(self, usuario, senha_atual: str, nova_senha: str) -> bool:
        """Altera senha do usuário (RF12, RNF03)."""
        return usuario.alterar_senha(senha_atual, nova_senha)

    def desativar(self, usuario) -> None:
        """Desativa conta do usuário no sistema (RF12)."""
        usuario.desativar()

    # --- Consultas ---

    def buscar_usuario(self, login: str):
        """Busca usuário pelo login."""
        return self._cache.buscar_usuario(login)

    def obter_perfil(self, usuario) -> str:
        """Retorna o perfil de acesso do usuário."""
        return usuario.perfil if usuario else ""
