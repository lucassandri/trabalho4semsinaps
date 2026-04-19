# view/tela_funcionario.py
# Tela de Funcionários (RF03)

import PySimpleGUI as sg


class TelaFuncionario:
    def __init__(self):
        sg.theme('LightBlue2')

    def abrir_menu(self) -> str:
        layout = [
            [sg.Text('Gerenciamento de Funcionários', font=('Helvetica', 14))],
            [sg.Button('Cadastrar Professor', size=(22, 1))],
            [sg.Button('Cadastrar Secretária', size=(22, 1))],
            [sg.Button('Consultar Funcionário', size=(22, 1))],
            [sg.Button('Listar Professores', size=(22, 1))],
            [sg.Button('Voltar', size=(22, 1))]
        ]
        janela = sg.Window('Funcionários', layout, element_justification='center')
        evento, _ = janela.read()
        janela.close()
        return evento if evento != sg.WIN_CLOSED else 'Voltar'

    def abrir_cadastro_professor(self) -> dict:
        layout = [
            [sg.Text('Cadastro de Professor', font=('Helvetica', 14))],
            [sg.Text('Nome*:', size=(18, 1)), sg.Input(key='-NOME-', size=(30, 1))],
            [sg.Text('CPF*:', size=(18, 1)), sg.Input(key='-CPF-', size=(30, 1))],
            [sg.Text('Matrícula Func.*:', size=(18, 1)), sg.Input(key='-MAT-', size=(30, 1))],
            [sg.Text('Telefone:', size=(18, 1)), sg.Input(key='-TEL-', size=(30, 1))],
            [sg.Text('E-mail:', size=(18, 1)), sg.Input(key='-EMAIL-', size=(30, 1))],
            [sg.Text('Formação:', size=(18, 1)), sg.Input(key='-FORM-', size=(30, 1))],
            [sg.Text('Titulação:', size=(18, 1)), sg.Input(key='-TIT-', size=(30, 1))],
            [sg.Button('Salvar'), sg.Button('Cancelar')]
        ]
        janela = sg.Window('Cadastrar Professor', layout)
        while True:
            evento, v = janela.read()
            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                janela.close()
                return None
            if evento == 'Salvar':
                if not v['-NOME-'].strip() or not v['-CPF-'].strip() or not v['-MAT-'].strip():
                    sg.popup_error('Nome, CPF e Matrícula são obrigatórios (*)')
                    continue
                janela.close()
                return {
                    'nome': v['-NOME-'].strip(), 'cpf': v['-CPF-'].strip(),
                    'matricula_funcionario': v['-MAT-'].strip(), 'cargo': 'Professor',
                    'telefone': v['-TEL-'].strip(), 'email': v['-EMAIL-'].strip(),
                    'formacao': v['-FORM-'].strip(), 'titulacao': v['-TIT-'].strip()
                }

    def abrir_cadastro_secretaria(self) -> dict:
        layout = [
            [sg.Text('Cadastro de Secretária', font=('Helvetica', 14))],
            [sg.Text('Nome*:', size=(18, 1)), sg.Input(key='-NOME-', size=(30, 1))],
            [sg.Text('CPF*:', size=(18, 1)), sg.Input(key='-CPF-', size=(30, 1))],
            [sg.Text('Matrícula Func.*:', size=(18, 1)), sg.Input(key='-MAT-', size=(30, 1))],
            [sg.Text('Setor:', size=(18, 1)), sg.Input(key='-SETOR-', size=(30, 1))],
            [sg.Button('Salvar'), sg.Button('Cancelar')]
        ]
        janela = sg.Window('Cadastrar Secretária', layout)
        while True:
            evento, v = janela.read()
            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                janela.close()
                return None
            if evento == 'Salvar':
                if not v['-NOME-'].strip() or not v['-CPF-'].strip() or not v['-MAT-'].strip():
                    sg.popup_error('Nome, CPF e Matrícula são obrigatórios (*)')
                    continue
                janela.close()
                return {
                    'nome': v['-NOME-'].strip(), 'cpf': v['-CPF-'].strip(),
                    'matricula_funcionario': v['-MAT-'].strip(), 'cargo': 'Secretaria',
                    'setor': v['-SETOR-'].strip()
                }

    def abrir_consulta(self) -> str:
        layout = [
            [sg.Text('Matrícula Func.*:'), sg.Input(key='-MAT-', size=(20, 1))],
            [sg.Button('Buscar'), sg.Button('Cancelar')]
        ]
        janela = sg.Window('Consultar Funcionário', layout)
        evento, v = janela.read()
        janela.close()
        if evento == 'Buscar' and v['-MAT-'].strip():
            return v['-MAT-'].strip()
        return None

    def exibir_dados(self, func):
        if func is None:
            sg.popup_error('Funcionário não encontrado.')
            return
        info = f"Nome: {func.nome}\nCPF: {func.cpf}\nMatrícula: {func.matricula_funcionario}\nCargo: {func.cargo}"
        sg.popup(info, title=f'Funcionário: {func.nome}')

    def abrir_listagem(self, lista: list):
        if not lista:
            sg.popup('Nenhum professor cadastrado.')
            return
        dados = [[p.nome, p.matricula_funcionario, p.formacao, len(p.materias)] for p in lista]
        layout = [
            [sg.Table(values=dados, headings=['Nome', 'Matrícula', 'Formação', 'Matérias'],
                      auto_size_columns=True, num_rows=min(15, len(dados)))],
            [sg.Button('Fechar')]
        ]
        janela = sg.Window('Professores', layout)
        janela.read()
        janela.close()

    def exibir_sucesso(self, msg): sg.popup(msg, title='Sucesso')
    def exibir_erro(self, msg): sg.popup_error(msg, title='Erro')
