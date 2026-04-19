# model/coordenador.py
# Classe Coordenador - herda de Funcionario (Herança)
# Dependência com Serie, Turma, Materia (cadastra - RF04)
# RN05: capacidade_maxima é campo obrigatório no cadastro de turma

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
        # Inicializa atributos herdados de Funcionario
        super().__init__(
            nome, cpf, data_nascimento, telefone, email,
            endereco, matricula_funcionario, "Coordenador", data_admissao
        )
        # Atributo protegido conforme diagrama
        self._area: str = area

    # --- Getters e Setters ---

    @property
    def area(self) -> str:
        return self._area

    @area.setter
    def area(self, valor: str):
        self._area = valor

    # --- Métodos públicos (diagrama de classes) ---

    def cadastrar_serie(self, dados: dict):
        """Cadastra nova série no sistema (RF04). Dependência com Serie.
        Args:
            dados: dicionário com codigo, nome, nivel.
        Returns:
            Objeto Serie criado ou None se código já existe.
        """
        from model.serie import Serie
        from cache.cache_manager import CacheManager
        cache = CacheManager()
        # Verifica se código já existe
        if cache.buscar_serie(dados.get("codigo", "")) is not None:
            return None
        # Cria a série
        serie = Serie(
            codigo=dados.get("codigo", ""),
            nome=dados.get("nome", ""),
            nivel=dados.get("nivel", "")
        )
        cache.adicionar_serie(serie)
        return serie

    def cadastrar_turma(self, dados_com_capacidade: dict):
        """Cadastra nova turma vinculada a série (RF04). Dependência com Turma.
        O campo capacidade_maxima é OBRIGATÓRIO (RN05).
        Args:
            dados_com_capacidade: dicionário com codigo, nome, turno,
                                  ano_letivo, capacidade_maxima, codigo_serie.
        Returns:
            Objeto Turma criado ou None se falhou.
        """
        from model.turma import Turma
        from cache.cache_manager import CacheManager
        cache = CacheManager()
        # Valida campo obrigatório capacidade_maxima (RN05)
        if "capacidade_maxima" not in dados_com_capacidade:
            return None
        # Busca a série para composição
        serie = cache.buscar_serie(dados_com_capacidade.get("codigo_serie", ""))
        if serie is None:
            return None
        # Cria a turma com capacidade máxima
        turma = Turma(
            codigo=dados_com_capacidade.get("codigo", ""),
            nome=dados_com_capacidade.get("nome", ""),
            turno=dados_com_capacidade.get("turno", ""),
            ano_letivo=dados_com_capacidade.get("ano_letivo", 0),
            capacidade_maxima=dados_com_capacidade["capacidade_maxima"]
        )
        # Composição: série compõe turma
        serie.adicionar_turma(turma)
        cache.adicionar_turma(turma)
        return turma

    def cadastrar_materia(self, dados: dict):
        """Cadastra nova matéria no sistema (RF04). Dependência com Materia.
        Args:
            dados: dicionário com codigo, nome, carga_horaria.
        Returns:
            Objeto Materia criado ou None se código já existe.
        """
        from model.materia import Materia
        from cache.cache_manager import CacheManager
        cache = CacheManager()
        if cache.buscar_materia(dados.get("codigo", "")) is not None:
            return None
        materia = Materia(
            codigo=dados.get("codigo", ""),
            nome=dados.get("nome", ""),
            carga_horaria=dados.get("carga_horaria", 0)
        )
        cache.adicionar_materia(materia)
        return materia

    def atribuir_professor_materia(self, professor, materia, turma) -> bool:
        """Atribui professor a matéria/turma (RF04).
        Args:
            professor: objeto Professor.
            materia: objeto Materia.
            turma: objeto Turma.
        Returns:
            True se atribuiu com sucesso.
        """
        # Associação: professor leciona matéria
        professor.adicionar_materia(materia)
        # Associação: turma oferece matéria
        turma.adicionar_materia(materia)
        return True

    def editar_serie(self, codigo: str, dados: dict) -> bool:
        """Edita dados de uma série existente (RF04).
        Args:
            codigo: código da série.
            dados: dicionário com campos a atualizar.
        Returns:
            True se editou, False se não encontrou.
        """
        from cache.cache_manager import CacheManager
        serie = CacheManager().buscar_serie(codigo)
        if serie is None:
            return False
        if "nome" in dados:
            serie.nome = dados["nome"]
        if "nivel" in dados:
            serie.nivel = dados["nivel"]
        return True

    def editar_turma(self, codigo: str, dados: dict) -> bool:
        """Edita dados de uma turma existente (RF04).
        Args:
            codigo: código da turma.
            dados: dicionário com campos a atualizar.
        Returns:
            True se editou, False se não encontrou.
        """
        from cache.cache_manager import CacheManager
        turma = CacheManager().buscar_turma(codigo)
        if turma is None:
            return False
        if "nome" in dados:
            turma.nome = dados["nome"]
        if "turno" in dados:
            turma.turno = dados["turno"]
        if "capacidade_maxima" in dados:
            turma.capacidade_maxima = dados["capacidade_maxima"]
        return True

    def editar_materia(self, codigo: str, dados: dict) -> bool:
        """Edita dados de uma matéria existente (RF04).
        Args:
            codigo: código da matéria.
            dados: dicionário com campos a atualizar.
        Returns:
            True se editou, False se não encontrou.
        """
        from cache.cache_manager import CacheManager
        materia = CacheManager().buscar_materia(codigo)
        if materia is None:
            return False
        if "nome" in dados:
            materia.nome = dados["nome"]
        if "carga_horaria" in dados:
            materia.carga_horaria = dados["carga_horaria"]
        return True
