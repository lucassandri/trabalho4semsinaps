# model/historico_escolar.py
# Classe HistoricoEscolar - Agregação:
#   Agregado por Aluno (Aluno possui HistoricoEscolar)
#   Agrega Boletim (HistoricoEscolar agrega Boletins)
# RF10: emitir histórico escolar completo

from datetime import date


class HistoricoEscolar:
    """Histórico escolar do aluno. Agrega boletins de diferentes anos."""

    def __init__(self, data_emissao: date = None):
        # Atributos protegidos conforme diagrama
        self._data_emissao: date = data_emissao
        # Agregação 1:1..* com Boletim
        self._boletins: list = []

    # --- Getters e Setters ---

    @property
    def data_emissao(self) -> date:
        return self._data_emissao

    @data_emissao.setter
    def data_emissao(self, valor: date):
        self._data_emissao = valor

    @property
    def boletins(self) -> list:
        return self._boletins

    # --- Métodos públicos (diagrama de classes) ---

    def adicionar_boletim(self, boletim) -> None:
        """Adiciona boletim ao histórico (Agregação: boletim continua existindo)."""
        if boletim not in self._boletins:
            self._boletins.append(boletim)

    def remover_boletim(self, boletim) -> None:
        """Remove boletim do histórico (Agregação: boletim não é destruído)."""
        if boletim in self._boletins:
            self._boletins.remove(boletim)

    def gerar_historico_completo(self) -> dict:
        """Gera histórico escolar completo com séries, médias e situações (RF10).
        Returns:
            Dicionário com dados completos do histórico:
            {
                'data_emissao': date,
                'registros': [
                    {'ano_letivo': int, 'media_final': float,
                     'frequencia': float, 'situacao': str}
                ]
            }
        """
        registros = []
        for boletim in self._boletins:
            registros.append({
                "ano_letivo": boletim.ano_letivo,
                "media_final": boletim.media_final,
                "frequencia": boletim.frequencia_percentual,
                "situacao": boletim.situacao
            })
        # Ordena por ano letivo
        registros.sort(key=lambda r: r["ano_letivo"])
        return {
            "data_emissao": self._data_emissao,
            "registros": registros
        }
