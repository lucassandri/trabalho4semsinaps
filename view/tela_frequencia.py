# view/tela_frequencia.py
# Tela de Frequência (RF06) - registra presença/falta, edita dia anterior

import PySimpleGUI as sg
from datetime import date


class TelaFrequencia:
    def __init__(self): sg.theme('LightBlue2')

    def abrir_registro(self, matriculas: list, materias: list) -> dict:
        """Registra frequência por presença OU falta (RF06)."""
        lm = [m.codigo for m in matriculas]
        lmat = [f"{m.codigo} - {m.nome}" for m in materias]
        layout = [
            [sg.Text('Registrar Frequência', font=('Helvetica', 14))],
            [sg.Text('Matrícula*:'), sg.Combo(lm, key='-MAT-', size=(30, 1))],
            [sg.Text('Matéria*:'), sg.Combo(lmat, key='-MATERIA-', size=(30, 1))],
            [sg.Text('Data Aula*:'), sg.Input(key='-DATA-', size=(12, 1), default_text=date.today().strftime('%d/%m/%Y')),
             sg.CalendarButton('...', target='-DATA-', format='%d/%m/%Y')],
            # RF06: registra por presença ou falta
            [sg.Text('Registro*:'), sg.Radio('Presença', 'REG', key='-PRES-', default=True),
             sg.Radio('Falta', 'REG', key='-FALTA-')],
            [sg.Text('Justificativa:'), sg.Input(key='-JUST-', size=(30, 1), tooltip='Apenas se falta')],
            [sg.Button('Registrar'), sg.Button('Cancelar')]
        ]
        j = sg.Window('Registrar Frequência', layout)
        while True:
            e, v = j.read()
            if e in (sg.WIN_CLOSED, 'Cancelar'): j.close(); return None
            if e == 'Registrar':
                if not v['-MAT-'] or not v['-MATERIA-'] or not v['-DATA-']:
                    sg.popup_error('Preencha todos os campos obrigatórios (*)'); continue
                try:
                    partes = v['-DATA-'].strip().split('/')
                    data_aula = date(int(partes[2]), int(partes[1]), int(partes[0]))
                except (ValueError, IndexError):
                    sg.popup_error('Data inválida. Use dd/mm/aaaa.'); continue
                presente = v['-PRES-']
                cod_materia = v['-MATERIA-'].split(' - ')[0]
                j.close()
                return {
                    'cod_matricula': v['-MAT-'], 'cod_materia': cod_materia,
                    'data_aula': data_aula, 'presente': presente,
                    'justificativa': v['-JUST-'].strip() if not presente else ''
                }

    def abrir_edicao(self, matriculas: list, materias: list) -> dict:
        """Edita registro de frequência de dia anterior (RF06)."""
        lm = [m.codigo for m in matriculas]
        lmat = [f"{m.codigo} - {m.nome}" for m in materias]
        layout = [
            [sg.Text('Editar Frequência (dia anterior)', font=('Helvetica', 14))],
            [sg.Text('Matrícula*:'), sg.Combo(lm, key='-MAT-', size=(30, 1))],
            [sg.Text('Matéria*:'), sg.Combo(lmat, key='-MATERIA-', size=(30, 1))],
            [sg.Text('Data da Aula*:'), sg.Input(key='-DATA-', size=(12, 1)),
             sg.CalendarButton('...', target='-DATA-', format='%d/%m/%Y')],
            [sg.Text('Corrigir para:'), sg.Radio('Presença', 'REG', key='-PRES-', default=True),
             sg.Radio('Falta', 'REG', key='-FALTA-')],
            [sg.Button('Salvar Edição'), sg.Button('Cancelar')]
        ]
        j = sg.Window('Editar Frequência', layout)
        while True:
            e, v = j.read()
            if e in (sg.WIN_CLOSED, 'Cancelar'): j.close(); return None
            if e == 'Salvar Edição':
                if not v['-MAT-'] or not v['-MATERIA-'] or not v['-DATA-']:
                    sg.popup_error('Preencha todos os campos obrigatórios (*)'); continue
                try:
                    partes = v['-DATA-'].strip().split('/')
                    data_aula = date(int(partes[2]), int(partes[1]), int(partes[0]))
                    # RF06: só permite editar dia anterior
                    if data_aula >= date.today():
                        sg.popup_error('Só é possível editar registros de dias anteriores (RF06).')
                        continue
                except (ValueError, IndexError):
                    sg.popup_error('Data inválida.'); continue
                cod_materia = v['-MATERIA-'].split(' - ')[0]
                j.close()
                return {
                    'cod_matricula': v['-MAT-'], 'cod_materia': cod_materia,
                    'data_aula': data_aula, 'presente': v['-PRES-']
                }

    def exibir_sucesso(self, msg): sg.popup(msg, title='Sucesso')
    def exibir_erro(self, msg): sg.popup_error(msg, title='Erro')
