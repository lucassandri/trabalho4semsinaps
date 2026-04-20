# controller/usuario_controller.py
# Controller do ator Usuario - operações de conta do próprio usuário (RF12)
# Autenticação e sessão → SistemaController
# Busca de usuário é infraestrutura interna, não operação de ator

class UsuarioController:
    """Operações do ator Usuario sobre sua própria conta (RF12)."""

    def alterar_senha(self, usuario, senha_atual: str, nova_senha: str) -> bool:
        """Altera senha do usuário autenticado (RF12, RNF03)."""
        return usuario.alterar_senha(senha_atual, nova_senha)

    def desativar(self, usuario) -> None:
        """Desativa conta do usuário no sistema (RF12)."""
        usuario.desativar()
