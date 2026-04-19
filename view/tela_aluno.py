# view/tela_aluno.py
# Tela de Alunos - cadastrar, editar, consultar (RF01)
# RNF01: campos obrigatórios sinalizados com *

import PySimpleGUI as sg


class TelaAluno:
    """Tela de gerenciamento de alunos."""

    def __init__(self):
        sg.theme('LightBlue2')

    def abrir_menu_aluno(self) -> str:
        """Abre submenu de alunos.
        Returns:
            Opção selecionada ou None.
        """
        layout = [
            [sg.Text('Gerenciamento de Alunos', font=('Helvetica', 14))],
            [sg.Button('Cadastrar Aluno', size=(20, 1))],
            [sg.Button('Editar Aluno', size=(20, 1))],
            [sg.Button('Consultar Aluno', size=(20, 1))],
            [sg.Button('Listar Alunos', size=(20, 1))],
            [sg.Button('Voltar', size=(20, 1))]
        ]
        janela = sg.Window('Alunos', layout, element_justification='center')
        evento, _ = janela.read()
        janela.close()
        return evento if evento != sg.WIN_CLOSED else 'Voltar'

    def abrir_cadastro(self) -> dict:
        """Abre janela de cadastro de aluno (RF01).
        Returns:
            Dicionário com dados ou None.
        """
        layout = [
            [sg.Text('Cadastro de Aluno', font=('Helvetica', 14))],
            [sg.Text('Nome*:', size=(18, 1)), sg.Input(key='-NOME-', size=(30, 1))],
            [sg.Text('CPF*:', size=(18, 1)), sg.Input(key='-CPF-', size=(30, 1))],
            [sg.Text('Data Nascimento:', size=(18, 1)), sg.Input(key='-DNASC-', size=(30, 1), tooltip='dd/mm/aaaa')],
            [sg.Text('Telefone:', size=(18, 1)), sg.Input(key='-TEL-', size=(30, 1))],
            [sg.Text('E-mail:', size=(18, 1)), sg.Input(key='-EMAIL-', size=(30, 1))],
            [sg.Text('Endereço:', size=(18, 1)), sg.Input(key='-END-', size=(30, 1))],
            [sg.Text('Responsável:', size=(18, 1)), sg.Input(key='-RESP-', size=(30, 1))],
            [sg.Text('Tel. Responsável:', size=(18, 1)), sg.Input(key='-TELRESP-', size=(30, 1))],
            [sg.Button('Salvar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        janela = sg.Window('Cadastrar Aluno', layout)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                janela.close()
                return None
            if evento == 'Salvar':
                # RNF01: valida campos obrigatórios
                if not valores['-NOME-'].strip() or not valores['-CPF-'].strip():
                    sg.popup_error('Nome e CPF são obrigatórios (*)', title='Erro')
                    continue
                janela.close()
                return {
                    'nome': valores['-NOME-'].strip(),
                    'cpf': valores['-CPF-'].strip(),
                    'telefone': valores['-TEL-'].strip(),
                    'email': valores['-EMAIL-'].strip(),
                    'endereco': valores['-END-'].strip(),
                    'responsavel': valores['-RESP-'].strip(),
                    'telefone_responsavel': valores['-TELRESP-'].strip()
                }

    def abrir_consulta(self) -> str:
        """Abre janela para informar CPF de consulta.
        Returns:
            CPF informado ou None.
        """
        layout = [
            [sg.Text('Consultar Aluno', font=('Helvetica', 14))],
            [sg.Text('CPF*:', size=(6, 1)), sg.Input(key='-CPF-', size=(25, 1))],
            [sg.Button('Buscar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        janela = sg.Window('Consultar Aluno', layout)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                janela.close()
                return None
            if evento == 'Buscar':
                cpf = valores['-CPF-'].strip()
                if not cpf:
                    sg.popup_error('CPF é obrigatório (*)', title='Erro')
                    continue
                janela.close()
                return cpf

    def exibir_dados_aluno(self, aluno):
        """Exibe dados de um aluno."""
        if aluno is None:
            sg.popup_error('Aluno não encontrado.', title='Erro')
            return
        info = (
            f"Nome: {aluno.nome}\n"
            f"CPF: {aluno.cpf}\n"
            f"Telefone: {aluno.telefone}\n"
            f"E-mail: {aluno.email}\n"
            f"Endereço: {aluno.endereco}\n"
            f"Responsável: {aluno.responsavel}\n"
            f"Tel. Responsável: {aluno.telefone_responsavel}\n"
            f"Matrículas: {len(aluno.matriculas)}"
        )
        sg.popup(info, title=f'Aluno: {aluno.nome}')

    def abrir_listagem(self, lista_alunos: list):
        """Exibe lista de alunos em tabela."""
        if not lista_alunos:
            sg.popup('Nenhum aluno cadastrado.', title='Listagem')
            return
        dados = [[a.nome, a.cpf, a.telefone, len(a.matriculas)] for a in lista_alunos]
        cabecalho = ['Nome', 'CPF', 'Telefone', 'Matrículas']
        layout = [
            [sg.Text('Alunos Cadastrados', font=('Helvetica', 14))],
            [sg.Table(values=dados, headings=cabecalho, auto_size_columns=True,
                      justification='left', num_rows=min(15, len(dados)))],
            [sg.Button('Fechar', size=(10, 1))]
        ]
        janela = sg.Window('Listar Alunos', layout)
        janela.read()
        janela.close()

    def abrir_edicao(self, aluno) -> dict:
        """Abre janela de edição com dados atuais do aluno.
        Returns:
            Dicionário com dados atualizados ou None.
        """
        if aluno is None:
            sg.popup_error('Aluno não encontrado.', title='Erro')
            return None
        layout = [
            [sg.Text(f'Editar Aluno: {aluno.nome}', font=('Helvetica', 14))],
            [sg.Text('Nome*:', size=(18, 1)), sg.Input(default_text=aluno.nome, key='-NOME-', size=(30, 1))],
            [sg.Text('Telefone:', size=(18, 1)), sg.Input(default_text=aluno.telefone, key='-TEL-', size=(30, 1))],
            [sg.Text('E-mail:', size=(18, 1)), sg.Input(default_text=aluno.email, key='-EMAIL-', size=(30, 1))],
            [sg.Text('Endereço:', size=(18, 1)), sg.Input(default_text=aluno.endereco, key='-END-', size=(30, 1))],
            [sg.Text('Responsável:', size=(18, 1)), sg.Input(default_text=aluno.responsavel, key='-RESP-', size=(30, 1))],
            [sg.Text('Tel. Responsável:', size=(18, 1)), sg.Input(default_text=aluno.telefone_responsavel, key='-TELRESP-', size=(30, 1))],
            [sg.Button('Salvar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        janela = sg.Window('Editar Aluno', layout)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                janela.close()
                return None
            if evento == 'Salvar':
                if not valores['-NOME-'].strip():
                    sg.popup_error('Nome é obrigatório (*)', title='Erro')
                    continue
                janela.close()
                return {
                    'nome': valores['-NOME-'].strip(),
                    'telefone': valores['-TEL-'].strip(),
                    'email': valores['-EMAIL-'].strip(),
                    'endereco': valores['-END-'].strip(),
                    'responsavel': valores['-RESP-'].strip(),
                    'telefone_responsavel': valores['-TELRESP-'].strip()
                }

    def exibir_sucesso(self, msg: str):
        sg.popup(msg, title='Sucesso')

    def exibir_erro(self, msg: str):
        sg.popup_error(msg, title='Erro')
