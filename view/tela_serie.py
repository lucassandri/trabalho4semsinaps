# view/tela_serie.py
# Tela de Séries (RF04)

import PySimpleGUI as sg


class TelaSerie:
    def __init__(self):
        sg.theme('LightBlue2')

    def abrir_cadastro(self) -> dict:
        layout = [
            [sg.Text('Cadastro de Série', font=('Helvetica', 14))],
            [sg.Text('Código*:', size=(10, 1)), sg.Input(key='-COD-', size=(20, 1))],
            [sg.Text('Nome*:', size=(10, 1)), sg.Input(key='-NOME-', size=(20, 1))],
            [sg.Text('Nível*:', size=(10, 1)), sg.Combo(['Fundamental', 'Médio'], key='-NIVEL-', size=(18, 1))],
            [sg.Button('Salvar'), sg.Button('Cancelar')]
        ]
        janela = sg.Window('Cadastrar Série', layout)
        while True:
            evento, v = janela.read()
            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                janela.close()
                return None
            if evento == 'Salvar':
                if not v['-COD-'].strip() or not v['-NOME-'].strip() or not v['-NIVEL-']:
                    sg.popup_error('Todos os campos são obrigatórios (*)')
                    continue
                janela.close()
                return {'codigo': v['-COD-'].strip(), 'nome': v['-NOME-'].strip(), 'nivel': v['-NIVEL-']}

    def abrir_listagem(self, lista: list):
        if not lista:
            sg.popup('Nenhuma série cadastrada.')
            return
        dados = [[s.codigo, s.nome, s.nivel, len(s.turmas)] for s in lista]
        layout = [
            [sg.Table(values=dados, headings=['Código', 'Nome', 'Nível', 'Turmas'],
                      auto_size_columns=True, num_rows=min(10, len(dados)))],
            [sg.Button('Fechar')]
        ]
        janela = sg.Window('Séries', layout)
        janela.read()
        janela.close()

    def exibir_sucesso(self, msg): sg.popup(msg, title='Sucesso')
    def exibir_erro(self, msg): sg.popup_error(msg, title='Erro')
