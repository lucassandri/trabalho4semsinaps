# view/tela_turma.py
# Tela de Turmas (RF04) - capacidade_maxima obrigatória (RN05)

import PySimpleGUI as sg


class TelaTurma:
    def __init__(self):
        sg.theme('LightBlue2')

    def abrir_cadastro(self, lista_series: list) -> dict:
        """Cadastro de turma com campo capacidade_maxima obrigatório (RN05 via RF04)."""
        nomes_series = [f"{s.codigo} - {s.nome}" for s in lista_series] if lista_series else []
        layout = [
            [sg.Text('Cadastro de Turma', font=('Helvetica', 14))],
            [sg.Text('Código*:', size=(18, 1)), sg.Input(key='-COD-', size=(20, 1))],
            [sg.Text('Nome*:', size=(18, 1)), sg.Input(key='-NOME-', size=(20, 1))],
            [sg.Text('Turno*:', size=(18, 1)), sg.Combo(['Matutino', 'Vespertino', 'Noturno'], key='-TURNO-')],
            [sg.Text('Ano Letivo*:', size=(18, 1)), sg.Input(key='-ANO-', size=(10, 1))],
            # RN05: capacidade_maxima é campo obrigatório
            [sg.Text('Capacidade Máxima*:', size=(18, 1)), sg.Input(key='-CAP-', size=(10, 1))],
            [sg.Text('Série*:', size=(18, 1)), sg.Combo(nomes_series, key='-SERIE-', size=(25, 1))],
            [sg.Button('Salvar'), sg.Button('Cancelar')]
        ]
        janela = sg.Window('Cadastrar Turma', layout)
        while True:
            evento, v = janela.read()
            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                janela.close()
                return None
            if evento == 'Salvar':
                # RNF01 + RN05: validação de campos obrigatórios
                if not all([v['-COD-'].strip(), v['-NOME-'].strip(), v['-TURNO-'],
                           v['-ANO-'].strip(), v['-CAP-'].strip(), v['-SERIE-']]):
                    sg.popup_error('Todos os campos são obrigatórios (*)\nCapacidade Máxima é obrigatória (RN05)')
                    continue
                try:
                    cap = int(v['-CAP-'].strip())
                    ano = int(v['-ANO-'].strip())
                    if cap <= 0:
                        sg.popup_error('Capacidade deve ser maior que zero.')
                        continue
                except ValueError:
                    sg.popup_error('Ano Letivo e Capacidade devem ser números inteiros.')
                    continue
                cod_serie = v['-SERIE-'].split(' - ')[0] if v['-SERIE-'] else ''
                janela.close()
                return {
                    'codigo': v['-COD-'].strip(), 'nome': v['-NOME-'].strip(),
                    'turno': v['-TURNO-'], 'ano_letivo': ano,
                    'capacidade_maxima': cap, 'codigo_serie': cod_serie
                }

    def abrir_listagem(self, lista: list):
        if not lista:
            sg.popup('Nenhuma turma cadastrada.')
            return
        dados = [[t.codigo, t.nome, t.turno, t.ano_letivo, t.total_alunos, t.capacidade_maxima] for t in lista]
        layout = [
            [sg.Table(values=dados, headings=['Código', 'Nome', 'Turno', 'Ano', 'Alunos', 'Capacidade'],
                      auto_size_columns=True, num_rows=min(10, len(dados)))],
            [sg.Button('Fechar')]
        ]
        janela = sg.Window('Turmas', layout)
        janela.read()
        janela.close()

    def exibir_sucesso(self, msg): sg.popup(msg, title='Sucesso')
    def exibir_erro(self, msg): sg.popup_error(msg, title='Erro')
