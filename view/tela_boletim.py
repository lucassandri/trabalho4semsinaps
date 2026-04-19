# view/tela_boletim.py
# Tela de Boletim (RF08, RF09) - exibe notas, média, frequência, situação

import PySimpleGUI as sg


class TelaBoletim:
    def __init__(self): sg.theme('LightBlue2')

    def abrir_selecao(self, matriculas: list) -> str:
        lm = [m.codigo for m in matriculas]
        if not lm: sg.popup('Nenhuma matrícula encontrada.'); return None
        layout = [
            [sg.Text('Selecione a matrícula:')],
            [sg.Combo(lm, key='-MAT-', size=(35, 1))],
            [sg.Button('Gerar Boletim'), sg.Button('Cancelar')]
        ]
        j = sg.Window('Boletim', layout)
        e, v = j.read(); j.close()
        if e == 'Gerar Boletim' and v['-MAT-']:
            return v['-MAT-']
        return None

    def exibir_boletim(self, boletim):
        """Exibe boletim completo (RF08)."""
        if boletim is None:
            sg.popup_error('Boletim não encontrado.'); return
        # Monta tabela de notas por matéria
        notas_por_materia = {}
        for nota in boletim.notas:
            nome_mat = nota.materia.nome if nota.materia else 'N/A'
            if nome_mat not in notas_por_materia:
                notas_por_materia[nome_mat] = {1: '-', 2: '-', 3: '-', 4: '-'}
            notas_por_materia[nome_mat][nota.bimestre] = str(nota.valor)
        dados = []
        for mat, bims in notas_por_materia.items():
            dados.append([mat, bims[1], bims[2], bims[3], bims[4]])
        # Determina cor da situação
        sit = boletim.situacao.upper()
        layout = [
            [sg.Text(f'Boletim - Ano Letivo: {boletim.ano_letivo}', font=('Helvetica', 14))],
            [sg.Table(values=dados, headings=['Matéria', 'B1', 'B2', 'B3', 'B4'],
                      auto_size_columns=True, num_rows=max(3, len(dados)), justification='center')],
            [sg.HorizontalSeparator()],
            [sg.Text(f'Média Final: {boletim.media_final:.1f}', font=('Helvetica', 12))],
            [sg.Text(f'Frequência: {boletim.frequencia_percentual:.1f}%', font=('Helvetica', 12))],
            [sg.Text(f'Situação: {sit}', font=('Helvetica', 14, 'bold'))],
            [sg.Button('Fechar')]
        ]
        j = sg.Window('Boletim Escolar', layout, element_justification='center')
        j.read(); j.close()

    def exibir_sucesso(self, msg): sg.popup(msg, title='Sucesso')
    def exibir_erro(self, msg): sg.popup_error(msg, title='Erro')
