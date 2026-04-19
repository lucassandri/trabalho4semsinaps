# model/coordenador.py
# Classe Coordenador - herda de Funcionario (Herança)
# Métodos de domínio apenas: sem CacheManager, sem lookups de persistência.
# O Controller é responsável por toda interação com o cache.

from datetime import date
from model.funcionario import Funcionario


class Coordenador(Funcionario):
    """Coordenador da escola. Cadastra séries, turmas, matérias e atribui professores."""

    def __init__(
        self,
        nome: str = "",
        cpf: str = "",
        data_nascimento: date = None,
        telefone: str = "",
        email: str = "",
        endereco: str = "",
        matricula_funcionario: str = "",
        data_admissao: date = None,
        area: str = ""
    ):
        super().__init__(
            nome, cpf, data_nascimento, telefone, email,
            endereco, matricula_funcionario, "Coordenador", data_admissao
        )
        self._area: str = area

    @property
    def area(self) -> str:
        return self._area

    @area.setter
    def area(self, valor: str):
        self._area = valor

    # --- Métodos de domínio (sem persistência) ---

    def criar_serie(self, dados: dict):
        """Cria e retorna objeto Serie (RF04).
        O Controller verifica duplicidade e persiste no cache.
        """
        from model.serie import Serie
        return Serie(
            codigo=dados.get("codigo", ""),
            nome=dados.get("nome", ""),
            nivel=dados.get("nivel", "")
        )

    def criar_turma(self, dados: dict, serie) -> object:
        """Cria Turma, vincula à Série e retorna o objeto (RF04, RN05).
        O campo capacidade_maxima é OBRIGATÓRIO (RN05).
        O Controller fornece a serie e persiste a turma no cache.
        Returns:
            Objeto Turma criado ou None se capacidade_maxima ausente.
        """
        from model.turma import Turma
        if "capacidade_maxima" not in dados:
            return None
        turma = Turma(
            codigo=dados.get("codigo", ""),
            nome=dados.get("nome", ""),
            turno=dados.get("turno", ""),
            ano_letivo=dados.get("ano_letivo", 0),
            capacidade_maxima=dados["capacidade_maxima"]
        )
        serie.adicionar_turma(turma)
        return turma

    def criar_materia(self, dados: dict):
        """Cria e retorna objeto Materia (RF04).
        O Controller verifica duplicidade e persiste no cache.
        """
        from model.materia import Materia
        return Materia(
            codigo=dados.get("codigo", ""),
            nome=dados.get("nome", ""),
            carga_horaria=dados.get("carga_horaria", 0)
        )

    def atribuir_professor_materia(self, professor, materia, turma) -> bool:
        """Atribui professor a matéria/turma (RF04).
        Returns:
            True se atribuiu com sucesso.
        """
        professor.adicionar_materia(materia)
        turma.adicionar_materia(materia)
        return True

    def atualizar_serie(self, serie, dados: dict) -> None:
        """Aplica dados editados ao objeto Serie (RF04).
        O Controller fornece o objeto e persiste a atualização.
        """
        if "nome" in dados:
            serie.nome = dados["nome"]
        if "nivel" in dados:
            serie.nivel = dados["nivel"]

    def atualizar_turma(self, turma, dados: dict) -> None:
        """Aplica dados editados ao objeto Turma (RF04).
        O Controller fornece o objeto e persiste a atualização.
        """
        if "nome" in dados:
            turma.nome = dados["nome"]
        if "turno" in dados:
            turma.turno = dados["turno"]
        if "capacidade_maxima" in dados:
            turma.capacidade_maxima = dados["capacidade_maxima"]

    def atualizar_materia(self, materia, dados: dict) -> None:
        """Aplica dados editados ao objeto Materia (RF04).
        O Controller fornece o objeto e persiste a atualização.
        """
        if "nome" in dados:
            materia.nome = dados["nome"]
        if "carga_horaria" in dados:
            materia.carga_horaria = dados["carga_horaria"]
