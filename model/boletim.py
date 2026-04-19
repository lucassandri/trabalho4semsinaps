# model/boletim.py
# Classe Boletim - Composição com Nota (Boletim compõe Notas)
# É composto por Matricula. Agregado por HistoricoEscolar.
# RF07: calcular média final e determinar situação
# RF08: gerar boletim com notas, média, frequência e situação
# RN01: aprovado = média >= 7.0 E frequência >= 75%
# RN02: recuperação = média entre 5.0 e 6.9 E frequência >= 75%
# RN03: reprovado = média < 5.0 OU frequência < 75%
# RN04: média = (N1 + N2 + N3 + N4) / 4


class Boletim:
    """Boletim do aluno. Agrupa notas e calcula média/situação."""

    def __init__(self):
        # Atributos protegidos conforme diagrama
        self._media_final: float = 0.0
        self._frequencia_percentual: float = 0.0
        self._situacao: str = ""
        self._ano_letivo: int = 0
        # Composição 1:1..* com Nota
        self._notas: list = []

    # --- Getters e Setters ---

    @property
    def media_final(self) -> float:
        return self._media_final

    @media_final.setter
    def media_final(self, valor: float):
        self._media_final = valor

    @property
    def frequencia_percentual(self) -> float:
        return self._frequencia_percentual

    @frequencia_percentual.setter
    def frequencia_percentual(self, valor: float):
        self._frequencia_percentual = valor

    @property
    def situacao(self) -> str:
        return self._situacao

    @situacao.setter
    def situacao(self, valor: str):
        self._situacao = valor

    @property
    def ano_letivo(self) -> int:
        return self._ano_letivo

    @ano_letivo.setter
    def ano_letivo(self, valor: int):
        self._ano_letivo = valor

    @property
    def notas(self) -> list:
        return self._notas

    # --- Métodos públicos (diagrama de classes) ---

    def adicionar_nota(self, nota) -> None:
        """Adiciona nota ao boletim (Composição)."""
        self._notas.append(nota)

    def remover_nota(self, nota) -> None:
        """Remove nota do boletim (Composição)."""
        if nota in self._notas:
            self._notas.remove(nota)

    def calcular_media_final(self) -> float:
        """Calcula a média final: (N1+N2+N3+N4)/4 (RF07, RN04).
        Agrupa notas por matéria, calcula média por matéria,
        depois faz a média geral de todas as matérias.
        Returns:
            Média final calculada.
        """
        if not self._notas:
            self._media_final = 0.0
            return self._media_final
        # Agrupa notas por matéria
        notas_por_materia = {}
        for nota in self._notas:
            chave = nota.materia.codigo if nota.materia else "sem_materia"
            if chave not in notas_por_materia:
                notas_por_materia[chave] = []
            notas_por_materia[chave].append(nota.valor)
        # Calcula média por matéria: (N1+N2+N3+N4)/4 (RN04)
        medias_materias = []
        for chave, valores in notas_por_materia.items():
            soma = sum(valores)
            qtd = len(valores)
            media_materia = soma / qtd if qtd > 0 else 0.0
            medias_materias.append(media_materia)
        # Média geral = média das médias por matéria
        if medias_materias:
            self._media_final = sum(medias_materias) / len(medias_materias)
        else:
            self._media_final = 0.0
        # Arredonda para uma casa decimal
        self._media_final = round(self._media_final, 1)
        return self._media_final

    def calcular_frequencia_percentual(self, frequencias: list) -> float:
        """Calcula o percentual de frequência do aluno.
        Args:
            frequencias: lista de objetos Frequencia da matrícula.
        Returns:
            Percentual de frequência (0.0 a 100.0).
        """
        if not frequencias:
            self._frequencia_percentual = 0.0
            return self._frequencia_percentual
        # Conta presenças e total de registros
        total = len(frequencias)
        presencas = sum(1 for f in frequencias if f.presente)
        self._frequencia_percentual = round((presencas / total) * 100, 1)
        return self._frequencia_percentual

    def determinar_situacao(self) -> str:
        """Determina situação do aluno (RF07, RN01-RN03).
        Ordem de avaliação refinada:
          1. Frequência < 75% → REPROVADO (RN03) - independente da média
          2. Média < 5.0 → REPROVADO (RN03)
          3. Média entre 5.0 e 6.9 com frequência >= 75% → RECUPERAÇÃO (RN02)
          4. Média >= 7.0 com frequência >= 75% → APROVADO (RN01)
        Returns:
            String com situação: 'aprovado', 'reprovado' ou 'recuperacao'.
        """
        freq = self._frequencia_percentual
        media = self._media_final
        # RN03: frequência < 75% → reprovado direto (independente da média)
        if freq < 75.0:
            self._situacao = "reprovado"
        # RN03: média < 5.0 → reprovado
        elif media < 5.0:
            self._situacao = "reprovado"
        # RN02: média entre 5.0 e 6.9 com frequência >= 75% → recuperação
        elif 5.0 <= media <= 6.9:
            self._situacao = "recuperacao"
        # RN01: média >= 7.0 com frequência >= 75% → aprovado
        else:
            self._situacao = "aprovado"
        return self._situacao
