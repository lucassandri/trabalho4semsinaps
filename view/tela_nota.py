# view/tela_nota.py
# Tela de Notas (RF05) - registrar notas bimestrais, RN06 (0.0 a 10.0)

import PySimpleGUI as sg


class TelaNota:
    def __init__(self): sg.theme('LightBlue2')

    def abrir_registro(self, matriculas: list, materias: list) -> dict:
        lm = [m.codigo for m in matriculas]
        lmat = [f"{m.codigo} - {m.nome}" for m in materias]
        layout = [
            [sg.Text('Registrar Nota', font=('Helvetica', 14))],
            [sg.Text('Matrícula*:'), sg.Combo(lm, key='-MAT-', size=(30, 1))],
            [sg.Text('Matéria*:'), sg.Combo(lmat, key='-MATERIA-', size=(30, 1))],
            [sg.Text('Bimestre*:'), sg.Combo([1, 2, 3, 4], key='-BIM-')],
            [sg.Text('Nota* (0-10):'), sg.Input(key='-NOTA-', size=(10, 1))],
            [sg.Button('Registrar'), sg.Button('Cancelar')]
        ]
        j = sg.Window('Registrar Nota', layout)
        while True:
            e, v = j.read()
            if e in (sg.WIN_CLOSED, 'Cancelar'): j.close(); return None
            if e == 'Registrar':
                if not v['-MAT-'] or not v['-MATERIA-'] or not v['-BIM-'] or not v['-NOTA-']:
                    sg.popup_error('Preencha todos os campos (*)'); continue
                try:
                    nota = float(v['-NOTA-'].strip().replace(',', '.'))
                    # RN06: nota entre 0.0 e 10.0
                    if not (0.0 <= nota <= 10.0):
                        sg.popup_error('Nota deve estar entre 0.0 e 10.0 (RN06)'); continue
                except ValueError:
                    sg.popup_error('Nota deve ser um número.'); continue
                cod_materia = v['-MATERIA-'].split(' - ')[0]
                j.close()
                return {
                    'cod_matricula': v['-MAT-'], 'cod_materia': cod_materia,
                    'bimestre': v['-BIM-'], 'valor': nota
                }

    def exibir_sucesso(self, msg): sg.popup(msg, title='Sucesso')
    def exibir_erro(self, msg): sg.popup_error(msg, title='Erro')
