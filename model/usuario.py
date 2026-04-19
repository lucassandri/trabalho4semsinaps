# model/usuario.py
# Classe Usuario - Associação 1:1 com Pessoa
# RF12: autenticação com login/senha, diferenciando perfis
# RNF03: senhas armazenadas com hash seguro

import hashlib


class Usuario:
    """Usuário do sistema. Controla autenticação e perfil de acesso."""

    def __init__(
        self,
        login: str = "",
        senha: str = "",
        perfil: str = "",
        ativo: bool = True
    ):
        # Atributos protegidos conforme diagrama
        self._login: str = login
        # RNF03: armazena senha como hash SHA-256
        self._senha_hash: str = self._gerar_hash(senha) if senha else ""
        self._perfil: str = perfil       # secretaria, professor, coordenador, aluno
        self._ativo: bool = ativo

    # --- Método privado para hash ---

    def _gerar_hash(self, senha: str) -> str:
        """Gera hash SHA-256 da senha (RNF03)."""
        return hashlib.sha256(senha.encode()).hexdigest()

    # --- Getters e Setters ---

    @property
    def login(self) -> str:
        return self._login

    @login.setter
    def login(self, valor: str):
        self._login = valor

    @property
    def senha_hash(self) -> str:
        return self._senha_hash

    @property
    def perfil(self) -> str:
        return self._perfil

    @perfil.setter
    def perfil(self, valor: str):
        self._perfil = valor

    @property
    def ativo(self) -> bool:
        return self._ativo

    @ativo.setter
    def ativo(self, valor: bool):
        self._ativo = valor

    # --- Métodos públicos (diagrama de classes) ---

    def autenticar(self, login: str, senha: str) -> bool:
        """Autentica usuário com login e senha (RF12).
        Compara hash da senha informada com hash armazenado (RNF03).
        Args:
            login: login informado.
            senha: senha em texto plano.
        Returns:
            True se credenciais válidas e usuário ativo.
        """
        hash_informado = self._gerar_hash(senha)
        return (
            self._login == login
            and self._senha_hash == hash_informado
            and self._ativo
        )

    def alterar_senha(self, senha_atual: str, nova_senha: str) -> bool:
        """Altera a senha do usuário (RF12).
        Args:
            senha_atual: senha atual em texto plano.
            nova_senha: nova senha em texto plano.
        Returns:
            True se alterou com sucesso, False se senha atual incorreta.
        """
        # Verifica se a senha atual confere
        if self._gerar_hash(senha_atual) != self._senha_hash:
            return False
        # Atualiza para nova senha com hash (RNF03)
        self._senha_hash = self._gerar_hash(nova_senha)
        return True

    def desativar(self) -> None:
        """Desativa o usuário no sistema (RF12)."""
        self._ativo = False
