# model/secretaria.py
# Classe Secretaria - herda de Funcionario (Herança)
# Dependência com Matricula (efetua - RF02), Aluno (cadastra - RF01),
# Funcionario (cadastra - RF03), HistoricoEscolar (emite - RF10)

from datetime import date
from model.funcionario import Funcionario


class Secretaria(Funcionario):
    """Secretária da escola. Gerencia matrículas, cadastros e relatórios."""

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
        setor: str = ""
    ):
        # Inicializa atributos herdados de Funcionario
        super().__init__(
            nome, cpf, data_nascimento, telefone, email,
            endereco, matricula_funcionario, "Secretaria", data_admissao
        )
        # Atributo protegido conforme diagrama
        self._setor: str = setor

    # --- Getters e Setters ---

    @property
    def setor(self) -> str:
        return self._setor

    @setor.setter
    def setor(self, valor: str):
        self._setor = valor

    # --- Métodos públicos (diagrama de classes) ---

    def cadastrar_aluno(self, dados: dict) -> bool:
        """Cadastra novo aluno no sistema (RF01). Dependência com Aluno.
        Args:
            dados: dicionário com nome, cpf, data_nascimento, telefone,
                   email, endereco, responsavel, telefone_responsavel.
        Returns:
            True se cadastrou, False se CPF já existe.
        """
        from model.aluno import Aluno
        from cache.cache_manager import CacheManager
        cache = CacheManager()
        # Verifica se CPF já existe no cache
        if cache.buscar_aluno(dados.get("cpf", "")) is not None:
            return False
        # Cria o aluno com os dados informados
        aluno = Aluno(
            nome=dados.get("nome", ""),
            cpf=dados.get("cpf", ""),
            data_nascimento=dados.get("data_nascimento"),
            telefone=dados.get("telefone", ""),
            email=dados.get("email", ""),
            endereco=dados.get("endereco", ""),
            responsavel=dados.get("responsavel", ""),
            telefone_responsavel=dados.get("telefone_responsavel", "")
        )
        # Adiciona ao cache
        cache.adicionar_aluno(aluno)
        return True

    def editar_aluno(self, cpf: str, dados: dict) -> bool:
        """Edita dados de um aluno existente (RF01). Dependência com Aluno.
        Args:
            cpf: CPF do aluno a ser editado.
            dados: dicionário com os campos a atualizar.
        Returns:
            True se editou, False se não encontrou.
        """
        from cache.cache_manager import CacheManager
        cache = CacheManager()
        aluno = cache.buscar_aluno(cpf)
        if aluno is None:
            return False
        # Atualiza os campos informados
        if "nome" in dados:
            aluno.nome = dados["nome"]
        if "telefone" in dados:
            aluno.telefone = dados["telefone"]
        if "email" in dados:
            aluno.email = dados["email"]
        if "endereco" in dados:
            aluno.endereco = dados["endereco"]
        if "responsavel" in dados:
            aluno.responsavel = dados["responsavel"]
        if "telefone_responsavel" in dados:
            aluno.telefone_responsavel = dados["telefone_responsavel"]
        # Atualiza no cache
        cache.atualizar_aluno(aluno)
        return True

    def consultar_aluno(self, cpf: str):
        """Consulta aluno pelo CPF (RF01). Dependência com Aluno.
        Args:
            cpf: CPF do aluno.
        Returns:
            Objeto Aluno ou None.
        """
        from cache.cache_manager import CacheManager
        return CacheManager().buscar_aluno(cpf)

    def cadastrar_funcionario(self, dados: dict) -> bool:
        """Cadastra novo funcionário no sistema (RF03). Dependência com Funcionario.
        Args:
            dados: dicionário com dados do funcionário.
        Returns:
            True se cadastrou, False se matrícula já existe.
        """
        from cache.cache_manager import CacheManager
        cache = CacheManager()
        matricula = dados.get("matricula_funcionario", "")
        if cache.buscar_professor(matricula) or cache.buscar_secretaria(matricula):
            return False
        # Determina tipo pelo cargo
        cargo = dados.get("cargo", "")
        if cargo.lower() == "professor":
            from model.professor import Professor
            func = Professor(
                nome=dados.get("nome", ""),
                cpf=dados.get("cpf", ""),
                data_nascimento=dados.get("data_nascimento"),
                telefone=dados.get("telefone", ""),
                email=dados.get("email", ""),
                endereco=dados.get("endereco", ""),
                matricula_funcionario=matricula,
                data_admissao=dados.get("data_admissao"),
                formacao=dados.get("formacao", ""),
                titulacao=dados.get("titulacao", "")
            )
            cache.adicionar_professor(func)
        else:
            func = Secretaria(
                nome=dados.get("nome", ""),
                cpf=dados.get("cpf", ""),
                data_nascimento=dados.get("data_nascimento"),
                telefone=dados.get("telefone", ""),
                email=dados.get("email", ""),
                endereco=dados.get("endereco", ""),
                matricula_funcionario=matricula,
                data_admissao=dados.get("data_admissao"),
                setor=dados.get("setor", "")
            )
            cache.adicionar_secretaria(func)
        return True

    def editar_funcionario(self, matricula: str, dados: dict) -> bool:
        """Edita dados de um funcionário (RF03). Dependência com Funcionario.
        Args:
            matricula: matrícula funcional.
            dados: dicionário com campos a atualizar.
        Returns:
            True se editou, False se não encontrou.
        """
        from cache.cache_manager import CacheManager
        cache = CacheManager()
        func = cache.buscar_professor(matricula) or cache.buscar_secretaria(matricula)
        if func is None:
            return False
        if "nome" in dados:
            func.nome = dados["nome"]
        if "telefone" in dados:
            func.telefone = dados["telefone"]
        if "email" in dados:
            func.email = dados["email"]
        if "endereco" in dados:
            func.endereco = dados["endereco"]
        return True

    def consultar_funcionario(self, matricula: str):
        """Consulta funcionário pela matrícula (RF03).
        Returns:
            Objeto Funcionario (Professor ou Secretaria) ou None.
        """
        from cache.cache_manager import CacheManager
        cache = CacheManager()
        return cache.buscar_professor(matricula) or cache.buscar_secretaria(matricula)

    def efetuar_matricula(self, aluno, turma):
        """Efetua matrícula de aluno em turma (RF02). Dependência com Matricula.
        Verifica capacidade máxima da turma (RN05).
        Args:
            aluno: objeto Aluno.
            turma: objeto Turma.
        Returns:
            Objeto Matricula criado ou None se turma cheia (RN05).
        """
        from model.matricula import Matricula
        from model.boletim import Boletim
        from cache.cache_manager import CacheManager
        # Verifica capacidade da turma (RN05)
        if not turma.verificar_capacidade():
            return None
        # Cria a matrícula
        codigo = f"MAT-{aluno.cpf}-{turma.codigo}"
        mat = Matricula(codigo=codigo, data_matricula=date.today(), status="ativa")
        # Composição: cria o boletim da matrícula
        boletim = mat.criar_boletim()
        boletim.ano_letivo = turma.ano_letivo
        # Composição: turma compõe matrícula
        turma.adicionar_matricula(mat)
        # Composição: aluno compõe matrícula
        aluno.adicionar_matricula(mat)
        # Adiciona ao cache
        CacheManager().adicionar_matricula(mat)
        return mat

    def cancelar_matricula(self, matricula) -> bool:
        """Cancela uma matrícula existente (RF02). Dependência com Matricula.
        Args:
            matricula: objeto Matricula.
        Returns:
            True se cancelou com sucesso.
        """
        matricula.cancelar()
        return True

    def transferir_matricula(self, matricula, turma_destino) -> bool:
        """Transfere matrícula para outra turma (RF02). Dependência com Matricula.
        Verifica capacidade da turma destino (RN05).
        Args:
            matricula: objeto Matricula.
            turma_destino: objeto Turma de destino.
        Returns:
            True se transferiu, False se turma destino cheia.
        """
        if not turma_destino.verificar_capacidade():
            return False
        matricula.transferir(turma_destino)
        turma_destino.adicionar_matricula(matricula)
        return True

    def emitir_historico(self, aluno):
        """Emite histórico escolar completo do aluno (RF10).
        Dependência com HistoricoEscolar.
        Args:
            aluno: objeto Aluno.
        Returns:
            Objeto HistoricoEscolar gerado.
        """
        from model.historico_escolar import HistoricoEscolar
        # Cria o histórico com data de emissão atual
        historico = HistoricoEscolar(data_emissao=date.today())
        # Agregação: adiciona todos os boletins das matrículas do aluno
        for mat in aluno.matriculas:
            if mat.boletim is not None:
                historico.adicionar_boletim(mat.boletim)
        # Agregação: aluno possui histórico
        aluno.adicionar_historico(historico)
        return historico

    def gerar_relatorio_turma(self, turma) -> list:
        """Gera relatório de alunos matriculados por turma (RF11).
        Args:
            turma: objeto Turma.
        Returns:
            Lista de dicionários com dados dos alunos.
        """
        relatorio = []
        for mat in turma.matriculas:
            # Busca o aluno dono da matrícula no cache
            from cache.cache_manager import CacheManager
            for aluno in CacheManager().listar_alunos():
                if mat in aluno.matriculas:
                    relatorio.append({
                        "aluno": aluno.nome,
                        "cpf": aluno.cpf,
                        "matricula": mat.codigo,
                        "status": mat.status
                    })
        return relatorio

    def gerar_relatorio_professores(self, serie) -> list:
        """Gera relatório de professores alocados por série/matéria (RF11).
        Args:
            serie: objeto Serie.
        Returns:
            Lista de dicionários com dados dos professores.
        """
        from cache.cache_manager import CacheManager
        relatorio = []
        professores = CacheManager().listar_professores()
        for turma in serie.turmas:
            for materia in turma.materias:
                for prof in professores:
                    if materia in prof.materias:
                        relatorio.append({
                            "professor": prof.nome,
                            "matricula": prof.matricula_funcionario,
                            "materia": materia.nome,
                            "turma": turma.nome,
                            "serie": serie.nome
                        })
        return relatorio
