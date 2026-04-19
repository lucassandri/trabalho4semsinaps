# controller/historico_controller.py
# Controller de HistoricoEscolar - opera sobre objetos HistoricoEscolar (RF10)

class HistoricoController:
    """Gerencia operações sobre HistoricoEscolar: geração e boletins agregados (RF10)."""

    # --- Geração (RF10) ---

    def gerar(self, historico) -> dict:
        """Gera e retorna o histórico escolar completo (RF10)."""
        return historico.gerar_historico_completo()

    # --- Boletins agregados ---

    def adicionar_boletim(self, historico, boletim) -> None:
        """Agrega boletim ao histórico (Agregação)."""
        historico.adicionar_boletim(boletim)

    def remover_boletim(self, historico, boletim) -> None:
        """Remove boletim do histórico (Agregação - boletim não é destruído)."""
        historico.remover_boletim(boletim)

    def listar_boletins(self, historico) -> list:
        """Lista boletins do histórico ordenados por ano letivo."""
        return sorted(historico.boletins, key=lambda b: b.ano_letivo)
