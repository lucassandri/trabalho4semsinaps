# view/tela_historico.py
# Tela de Histórico Escolar (RF09, RF10)
# A view recebe apenas dados prontos (dict) do controller — não acessa o Model.

import PySimpleGUI as sg


class TelaHistorico:
    def __init__(self): sg.theme('LightBlue2')

    def solicitar_cpf(self) -> str:
        layout = [
            [sg.Text('Emitir Histórico Escolar', font=('Helvetica', 14))],
            [sg.Text('CPF do Aluno*:'), sg.Input(key='-CPF-', size=(20, 1))],
            [sg.Button('Emitir'), sg.Button('Cancelar')]
        ]
        j = sg.Window('Histórico', layout)
        e, v = j.read(); j.close()
        if e == 'Emitir' and v['-CPF-'].strip():
            return v['-CPF-'].strip()
        return None

    def exibir_historico(self, dados_hist: dict, nome_aluno: str = ''):
        """Exibe histórico escolar completo (RF10).
        Args:
            dados_hist: dicionário retornado por HistoricoController.gerar()
                        {'data_emissao': date, 'registros': [...]}
            nome_aluno: nome do aluno para o título.
        """
        if dados_hist is None:
            sg.popup_error('Histórico não encontrado.'); return
        registros = dados_hist.get('registros', [])
        if not registros:
            sg.popup('Nenhum registro no histórico.'); return
        dados = [
            [r['ano_letivo'], r['media_final'], f"{r['frequencia']:.1f}%", r['situacao'].upper()]
            for r in registros
        ]
        layout = [
            [sg.Text(f'Histórico Escolar - {nome_aluno}', font=('Helvetica', 14))],
            [sg.Text(f'Data Emissão: {dados_hist["data_emissao"]}')],
            [sg.Table(values=dados, headings=['Ano', 'Média', 'Frequência', 'Situação'],
                      auto_size_columns=True, num_rows=max(3, len(dados)))],
            [sg.Button('Fechar')]
        ]
        j = sg.Window('Histórico Escolar', layout, element_justification='center')
        j.read(); j.close()

    def exibir_sucesso(self, msg): sg.popup(msg, title='Sucesso')
    def exibir_erro(self, msg): sg.popup_error(msg, title='Erro')
