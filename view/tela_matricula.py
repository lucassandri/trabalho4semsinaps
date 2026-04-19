# view/tela_matricula.py
# Tela de Matrículas (RF02) - efetuar, cancelar, transferir

import PySimpleGUI as sg


class TelaMatricula:
    def __init__(self): sg.theme('LightBlue2')

    def abrir_menu(self) -> str:
        layout = [
            [sg.Text('Gerenciamento de Matrículas', font=('Helvetica', 14))],
            [sg.Button('Efetuar Matrícula', size=(22, 1))],
            [sg.Button('Cancelar Matrícula', size=(22, 1))],
            [sg.Button('Transferir Matrícula', size=(22, 1))],
            [sg.Button('Listar Matrículas', size=(22, 1))],
            [sg.Button('Voltar', size=(22, 1))]
        ]
        j = sg.Window('Matrículas', layout, element_justification='center')
        e, _ = j.read(); j.close()
        return e if e != sg.WIN_CLOSED else 'Voltar'

    def abrir_efetuar(self, alunos: list, turmas: list) -> tuple:
        la = [f"{a.cpf} - {a.nome}" for a in alunos]
        lt = [f"{t.codigo} - {t.nome} ({t.total_alunos}/{t.capacidade_maxima})" for t in turmas]
        layout = [
            [sg.Text('Efetuar Matrícula', font=('Helvetica', 14))],
            [sg.Text('Aluno*:'), sg.Combo(la, key='-ALUNO-', size=(35, 1))],
            [sg.Text('Turma*:'), sg.Combo(lt, key='-TURMA-', size=(35, 1))],
            [sg.Button('Matricular'), sg.Button('Cancelar')]
        ]
        j = sg.Window('Efetuar Matrícula', layout)
        while True:
            e, v = j.read()
            if e in (sg.WIN_CLOSED, 'Cancelar'): j.close(); return None, None
            if e == 'Matricular':
                if not v['-ALUNO-'] or not v['-TURMA-']:
                    sg.popup_error('Selecione aluno e turma.'); continue
                cpf = v['-ALUNO-'].split(' - ')[0]
                cod = v['-TURMA-'].split(' - ')[0]
                j.close(); return cpf, cod

    def abrir_cancelar(self, matriculas: list) -> str:
        lm = [f"{m.codigo} - {m.status}" for m in matriculas if m.status == 'ativa']
        if not lm: sg.popup('Nenhuma matrícula ativa.'); return None
        layout = [
            [sg.Text('Cancelar Matrícula')],
            [sg.Combo(lm, key='-MAT-', size=(40, 1))],
            [sg.Button('Confirmar Cancelamento'), sg.Button('Voltar')]
        ]
        j = sg.Window('Cancelar Matrícula', layout)
        e, v = j.read(); j.close()
        if e == 'Confirmar Cancelamento' and v['-MAT-']:
            return v['-MAT-'].split(' - ')[0]
        return None

    def abrir_transferir(self, matriculas: list, turmas: list) -> tuple:
        lm = [f"{m.codigo}" for m in matriculas if m.status == 'ativa']
        lt = [f"{t.codigo} - {t.nome} ({t.total_alunos}/{t.capacidade_maxima})" for t in turmas]
        layout = [
            [sg.Text('Transferir Matrícula')],
            [sg.Text('Matrícula:'), sg.Combo(lm, key='-MAT-', size=(35, 1))],
            [sg.Text('Turma destino:'), sg.Combo(lt, key='-TURMA-', size=(35, 1))],
            [sg.Button('Transferir'), sg.Button('Cancelar')]
        ]
        j = sg.Window('Transferir Matrícula', layout)
        e, v = j.read(); j.close()
        if e == 'Transferir' and v['-MAT-'] and v['-TURMA-']:
            return v['-MAT-'], v['-TURMA-'].split(' - ')[0]
        return None, None

    def abrir_listagem(self, matriculas: list):
        if not matriculas: sg.popup('Nenhuma matrícula.'); return
        dados = [[m.codigo, m.status, str(m.data_matricula)] for m in matriculas]
        layout = [[sg.Table(values=dados, headings=['Código', 'Status', 'Data'], auto_size_columns=True, num_rows=min(15, len(dados)))], [sg.Button('Fechar')]]
        j = sg.Window('Matrículas', layout); j.read(); j.close()

    def exibir_sucesso(self, msg): sg.popup(msg, title='Sucesso')
    def exibir_erro(self, msg): sg.popup_error(msg, title='Erro')
