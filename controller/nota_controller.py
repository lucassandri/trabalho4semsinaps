# controller/nota_controller.py
# Controller de Nota - opera sobre objetos Nota (RF05, RN06)

from datetime import date


class NotaController:
    """Gerencia operações sobre Nota: criação e validação (RF05, RN06)."""

    # --- Criação ---

    def criar(self, bimestre: int, valor: float, materia, data_lancamento: date = None):
        """Cria e retorna um objeto Nota (RF05).
        Args:
            bimestre: número do bimestre (1 a 4).
            valor: valor da nota (0.0 a 10.0).
            materia: objeto Materia associado.
            data_lancamento: data de lançamento (padrão: hoje).
        Returns:
            Objeto Nota criado ou None se valor inválido (RN06).
        """
        from model.nota import Nota
        nota = Nota(
            bimestre=bimestre,
            valor=valor,
            data_lancamento=data_lancamento or date.today()
        )
        nota.materia = materia
        if not nota.validar_nota():
            return None
        return nota

    # --- Validação (RN06) ---

    def validar(self, nota) -> bool:
        """Valida se a nota está entre 0.0 e 10.0 (RN06)."""
        return nota.validar_nota()
