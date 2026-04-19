# model/professor.py
# Classe Professor - herda de Funcionario (Herança)
# Associação 1:1..* com Materia (leciona)
# Dependência com Nota (registra - RF05) e Frequencia (registra/edita - RF06)

from datetime import date
from model.funcionario import Funcionario


class Professor(Funcionario):
    """Professor da escola. Registra notas e frequências."""

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
        formacao: str = "",
        titulacao: str = ""
    ):
        # Inicializa atributos herdados de Funcionario
        super().__init__(
            nome, cpf, data_nascimento, telefone, email,
            endereco, matricula_funcionario, "Professor", data_admissao
        )
        # Atributos protegidos conforme diagrama
        self._formacao: str = formacao
        self._titulacao: str = titulacao
        # Associação 1:1..* com Materia
        self._materias: list = []

    # --- Getters e Setters ---

    @property
    def formacao(self) -> str:
        return self._formacao

    @formacao.setter
    def formacao(self, valor: str):
        self._formacao = valor

    @property
    def titulacao(self) -> str:
        return self._titulacao

    @titulacao.setter
    def titulacao(self, valor: str):
        self._titulacao = valor

    @property
    def materias(self) -> list:
        return self._materias

    # --- Métodos públicos (diagrama de classes) ---

    def registrar_nota(self, matricula, materia, bimestre: int, valor: float) -> bool:
        """Registra nota bimestral de um aluno em uma matéria (RF05).
        Dependência com Nota. Valida nota via RN06 (0.0 a 10.0).
        Args:
            matricula: objeto Matricula do aluno.
            materia: objeto Materia referente à nota.
            bimestre: número do bimestre (1 a 4).
            valor: valor da nota (0.0 a 10.0).
        Returns:
            True se registrou com sucesso, False se falhou.
        """
        from model.nota import Nota
        # Cria a nota com os dados informados
        nota = Nota(bimestre=bimestre, valor=valor, data_lancamento=date.today())
        # Associação: nota referente a uma matéria
        nota.materia = materia
        # Valida a nota conforme RN06
        if not nota.validar_nota():
            return False
        # Composição: nota compõe o boletim da matrícula
        if matricula.boletim is not None:
            matricula.boletim.adicionar_nota(nota)
            return True
        return False

    def registrar_frequencia(self, matricula, materia, data_aula: date, presente: bool) -> bool:
        """Registra frequência de um aluno por aula (RF06).
        Dependência com Frequencia. Registra presença OU falta.
        Args:
            matricula: objeto Matricula do aluno.
            materia: objeto Materia da aula.
            data_aula: data da aula.
            presente: True = presença, False = falta.
        Returns:
            True se registrou com sucesso, False se falhou.
        """
        from model.frequencia import Frequencia
        # Cria o registro de frequência
        freq = Frequencia(data_aula=data_aula, presente=presente)
        # Associação: frequência referente a uma matéria
        freq.materia = materia
        # Registra presença ou falta conforme RF06
        if presente:
            freq.registrar_presenca()
        else:
            freq.registrar_falta("")
        # Composição: frequência compõe a matrícula
        matricula.adicionar_frequencia(freq)
        return True

    def editar_frequencia(self, matricula, materia, data_aula: date, presente: bool) -> bool:
        """Edita registro de frequência de um dia anterior (RF06).
        Professor pode corrigir erro de registro anterior.
        Args:
            matricula: objeto Matricula do aluno.
            materia: objeto Materia da aula.
            data_aula: data da aula a ser editada.
            presente: novo valor de presença.
        Returns:
            True se editou com sucesso, False se não encontrou ou data inválida.
        """
        # Busca o registro de frequência na matrícula
        for freq in matricula.frequencias:
            if freq.data_aula == data_aula and freq.materia == materia:
                # Valida se a edição é permitida (dia anterior)
                if freq.validar_edicao(data_aula):
                    freq.editar_registro(presente, freq.justificativa)
                    return True
                return False
        return False

    def adicionar_materia(self, materia) -> None:
        """Adiciona matéria à lista de matérias lecionadas (Associação)."""
        if materia not in self._materias:
            self._materias.append(materia)

    def remover_materia(self, materia) -> None:
        """Remove matéria da lista de matérias lecionadas (Associação)."""
        if materia in self._materias:
            self._materias.remove(materia)
