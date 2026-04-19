# view/tela_materia.py
import PySimpleGUI as sg

class TelaMateria:
    def __init__(self): sg.theme('LightBlue2')

    def abrir_cadastro(self) -> dict:
        layout = [
            [sg.Text('Cadastro de Matéria', font=('Helvetica', 14))],
            [sg.Text('Código*:', size=(15, 1)), sg.Input(key='-COD-', size=(20, 1))],
            [sg.Text('Nome*:', size=(15, 1)), sg.Input(key='-NOME-', size=(20, 1))],
            [sg.Text('Carga Horária*:', size=(15, 1)), sg.Input(key='-CH-', size=(10, 1))],
            [sg.Button('Salvar'), sg.Button('Cancelar')]
        ]
        janela = sg.Window('Cadastrar Matéria', layout)
        while True:
            evento, v = janela.read()
            if evento in (sg.WIN_CLOSED, 'Cancelar'): janela.close(); return None
            if evento == 'Salvar':
                if not v['-COD-'].strip() or not v['-NOME-'].strip() or not v['-CH-'].strip():
                    sg.popup_error('Todos os campos são obrigatórios (*)'); continue
                try: ch = int(v['-CH-'].strip())
                except ValueError: sg.popup_error('Carga Horária deve ser número.'); continue
                janela.close()
                return {'codigo': v['-COD-'].strip(), 'nome': v['-NOME-'].strip(), 'carga_horaria': ch}

    def abrir_listagem(self, lista):
        if not lista: sg.popup('Nenhuma matéria cadastrada.'); return
        dados = [[m.codigo, m.nome, m.carga_horaria] for m in lista]
        layout = [[sg.Table(values=dados, headings=['Código', 'Nome', 'Carga Horária'], auto_size_columns=True, num_rows=min(10, len(dados)))], [sg.Button('Fechar')]]
        j = sg.Window('Matérias', layout); j.read(); j.close()

    def exibir_sucesso(self, msg): sg.popup(msg, title='Sucesso')
    def exibir_erro(self, msg): sg.popup_error(msg, title='Erro')
