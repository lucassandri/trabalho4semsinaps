# view/tela_login.py
# Tela de Login (RF12) - autenticação com login/senha

import PySimpleGUI as sg


class TelaLogin:
    """Tela de login do sistema."""

    def __init__(self):
        sg.theme('LightBlue2')

    def abrir(self) -> tuple:
        """Abre janela de login.
        Returns:
            Tupla (login, senha) ou (None, None) se cancelou.
        """
        layout = [
            [sg.Text('Sistema de Gestão Escolar', font=('Helvetica', 16), justification='center', expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Text('Login*:', size=(10, 1)), sg.Input(key='-LOGIN-', size=(25, 1))],
            [sg.Text('Senha*:', size=(10, 1)), sg.Input(key='-SENHA-', password_char='*', size=(25, 1))],
            [sg.Button('Entrar', size=(10, 1)), sg.Button('Sair', size=(10, 1))]
        ]
        janela = sg.Window('Login', layout, finalize=True, element_justification='center')
        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, 'Sair'):
                janela.close()
                return None, None
            if evento == 'Entrar':
                login = valores['-LOGIN-'].strip()
                senha = valores['-SENHA-'].strip()
                # RNF01: validação de campos obrigatórios
                if not login or not senha:
                    sg.popup_error('Preencha todos os campos obrigatórios (*)', title='Erro')
                    continue
                janela.close()
                return login, senha

    def exibir_erro_login(self):
        """Exibe erro de autenticação."""
        sg.popup_error('Login ou senha inválidos.', title='Erro de autenticação')

    def exibir_mensagem(self, titulo: str, mensagem: str):
        """Exibe mensagem genérica."""
        sg.popup(mensagem, title=titulo)
