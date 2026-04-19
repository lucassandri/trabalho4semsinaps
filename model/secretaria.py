# model/secretaria.py
# Classe Secretaria - herda de Funcionario (Herança)
# Métodos de domínio apenas: sem CacheManager, sem lookups de persistência.
# O Controller é responsável por toda interação com o cache.

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
        super().__init__(
            nome, cpf, data_nascimento, telefone, email,
            endereco, matricula_funcionario, "Secretaria", data_admissao
        )
        self._setor: str = setor

    @property
    def setor(self) -> str:
        return self._setor

    @setor.setter
    def setor(self, valor: str):
        self._setor = valor

    # --- Métodos de domínio (sem persistência) ---

    def criar_aluno(self, dados: dict):
        """Cria e retorna objeto Aluno com os dados informados (RF01).
        O Controller verifica duplicidade e persiste no cache.
        """
        from model.aluno import Aluno
        return Aluno(
            nome=dados.get("nome", ""),
            cpf=dados.get("cpf", ""),
            data_nascimento=dados.get("data_nascimento"),
            telefone=dados.get("telefone", ""),
            email=dados.get("email", ""),
            endereco=dados.get("endereco", ""),
            responsavel=dados.get("responsavel", ""),
            telefone_responsavel=dados.get("telefone_responsavel", "")
        )

    def atualizar_aluno(self, aluno, dados: dict) -> None:
        """Aplica dados editados ao objeto Aluno (RF01).
        O Controller fornece o objeto e persiste a atualização.
        """
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

    def criar_funcionario(self, dados: dict):
        """Cria e retorna Professor ou Secretaria com os dados informados (RF03).
        O Controller verifica duplicidade e persiste no cache.
        """
        cargo = dados.get("cargo", "")
        matricula = dados.get("matricula_funcionario", "")
        if cargo.lower() == "professor":
            from model.professor import Professor
            return Professor(
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
        return Secretaria(
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

    def atualizar_funcionario(self, func, dados: dict) -> None:
        """Aplica dados editados ao objeto Funcionario (RF03).
        O Controller fornece o objeto e persiste a atualização.
        """
        if "nome" in dados:
            func.nome = dados["nome"]
        if "telefone" in dados:
            func.telefone = dados["telefone"]
        if "email" in dados:
            func.email = dados["email"]
        if "endereco" in dados:
            func.endereco = dados["endereco"]

    def efetuar_matricula(self, aluno, turma):
        """Cria Matrícula e vincula ao Aluno e Turma (RF02, RN05).
        Verifica capacidade da turma. O Controller persiste a matrícula no cache.
        Returns:
            Objeto Matricula criado ou None se turma cheia (RN05).
        """
        from model.matricula import Matricula
        if not turma.verificar_capacidade():
            return None
        codigo = f"MAT-{aluno.cpf}-{turma.codigo}"
        mat = Matricula(codigo=codigo, data_matricula=date.today(), status="ativa")
        boletim = mat.criar_boletim()
        boletim.ano_letivo = turma.ano_letivo
        turma.adicionar_matricula(mat)
        aluno.adicionar_matricula(mat)
        return mat

    def cancelar_matricula(self, matricula) -> None:
        """Cancela a matrícula (RF02)."""
        matricula.cancelar()

    def transferir_matricula(self, matricula, turma_destino) -> bool:
        """Transfere matrícula para outra turma (RF02, RN05).
        Returns:
            True se transferiu, False se turma destino cheia.
        """
        if not turma_destino.verificar_capacidade():
            return False
        matricula.transferir(turma_destino)
        turma_destino.adicionar_matricula(matricula)
        return True

    def emitir_historico(self, aluno):
        """Cria HistoricoEscolar com os boletins do aluno (RF10).
        O Controller fornece o aluno; nenhum acesso ao cache aqui.
        Returns:
            Objeto HistoricoEscolar gerado.
        """
        from model.historico_escolar import HistoricoEscolar
        historico = HistoricoEscolar(data_emissao=date.today())
        for mat in aluno.matriculas:
            if mat.boletim is not None:
                historico.adicionar_boletim(mat.boletim)
        aluno.adicionar_historico(historico)
        return historico

    def gerar_relatorio_turma(self, turma, alunos: list) -> list:
        """Gera relatório de alunos matriculados por turma (RF11).
        Recebe lista de alunos do Controller (sem acesso ao cache).
        Returns:
            Lista de dicionários com dados dos alunos.
        """
        relatorio = []
        for mat in turma.matriculas:
            for aluno in alunos:
                if mat in aluno.matriculas:
                    relatorio.append({
                        "aluno": aluno.nome,
                        "cpf": aluno.cpf,
                        "matricula": mat.codigo,
                        "status": mat.status
                    })
        return relatorio

    def gerar_relatorio_professores(self, serie, professores: list) -> list:
        """Gera relatório de professores por série/matéria (RF11).
        Recebe lista de professores do Controller (sem acesso ao cache).
        Returns:
            Lista de dicionários com dados dos professores.
        """
        relatorio = []
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
