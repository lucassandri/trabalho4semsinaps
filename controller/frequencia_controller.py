# controller/frequencia_controller.py
# Controller de Frequencia - opera sobre objetos Frequencia (RF06)

from datetime import date


class FrequenciaController:
    """Gerencia operações sobre Frequencia: criação e edição (RF06)."""

    # --- Criação ---

    def criar(self, data_aula: date, presente: bool, materia, justificativa: str = ""):
        """Cria e retorna um objeto Frequencia (RF06).
        Args:
            data_aula: data da aula.
            presente: True = presença, False = falta.
            materia: objeto Materia associado.
            justificativa: motivo da falta (opcional).
        Returns:
            Objeto Frequencia criado com o registro já aplicado.
        """
        from model.frequencia import Frequencia
        freq = Frequencia(data_aula=data_aula, presente=presente,
                          justificativa=justificativa)
        freq.materia = materia
        if presente:
            freq.registrar_presenca()
        else:
            freq.registrar_falta(justificativa)
        return freq

    # --- Edição (RF06) ---

    def editar(self, frequencia, presente: bool, justificativa: str = "") -> bool:
        """Edita registro de frequência se a data for anterior a hoje (RF06).
        Returns:
            True se editou, False se a data não permite edição.
        """
        if not frequencia.validar_edicao(frequencia.data_aula):
            return False
        frequencia.editar_registro(presente, justificativa)
        return True

    def validar_edicao(self, frequencia) -> bool:
        """Verifica se a edição da frequência é permitida (RF06)."""
        return frequencia.validar_edicao(frequencia.data_aula)
