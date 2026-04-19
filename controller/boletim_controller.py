# controller/boletim_controller.py
# Controller de Boletim - opera sobre objetos Boletim (RF07, RF08)

class BoletimController:
    """Gerencia operações sobre Boletim: cálculo de média, frequência e situação (RF07, RF08)."""

    # --- Cálculos (RF07) ---

    def calcular_media(self, boletim) -> float:
        """Calcula e retorna a média final do boletim (RF07, RN04)."""
        return boletim.calcular_media_final()

    def calcular_frequencia(self, boletim, frequencias: list) -> float:
        """Calcula e retorna o percentual de frequência (RF07)."""
        return boletim.calcular_frequencia_percentual(frequencias)

    def determinar_situacao(self, boletim) -> str:
        """Determina e retorna a situação do aluno (RF07, RN01-RN03)."""
        return boletim.determinar_situacao()

    def gerar(self, boletim, frequencias: list):
        """Executa todos os cálculos e retorna o boletim atualizado (RF08).
        Calcula média, frequência e determina situação em sequência.
        Returns:
            Objeto Boletim com todos os campos atualizados.
        """
        boletim.calcular_media_final()
        boletim.calcular_frequencia_percentual(frequencias)
        boletim.determinar_situacao()
        return boletim

    # --- Notas ---

    def adicionar_nota(self, boletim, nota) -> None:
        """Adiciona nota ao boletim (Composição)."""
        boletim.adicionar_nota(nota)

    def remover_nota(self, boletim, nota) -> None:
        """Remove nota do boletim (Composição)."""
        boletim.remover_nota(nota)

    def listar_notas(self, boletim) -> list:
        """Lista notas do boletim."""
        return boletim.notas
