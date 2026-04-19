# view/tela_menu.py
# Menu principal - opções diferenciadas por perfil (RF12)

import PySimpleGUI as sg


class TelaMenu:
    """Menu principal do sistema com opções por perfil."""

    def __init__(self):
        sg.theme('LightBlue2')

    def abrir(self, perfil: str, nome: str) -> str:
        """Abre menu principal conforme perfil logado.
        Args:
            perfil: perfil do usuário (secretaria, professor, coordenador, aluno).
            nome: nome do usuário logado.
        Returns:
            String com opção selecionada ou None.
        """
        # Monta botões conforme perfil
        botoes = self._obter_botoes(perfil)
        layout = [
            [sg.Text(f'Bem-vindo(a), {nome}', font=('Helvetica', 14))],
            [sg.Text(f'Perfil: {perfil.upper()}', font=('Helvetica', 10))],
            [sg.HorizontalSeparator()],
        ]
        # Adiciona botões em linhas de 2
        for i in range(0, len(botoes), 2):
            linha = [sg.Button(botoes[i], size=(25, 2))]
            if i + 1 < len(botoes):
                linha.append(sg.Button(botoes[i + 1], size=(25, 2)))
            layout.append(linha)
        layout.append([sg.HorizontalSeparator()])
        layout.append([sg.Button('Logout', size=(15, 1)), sg.Button('Sair', size=(15, 1))])

        janela = sg.Window('Menu Principal', layout, finalize=True)
        while True:
            evento, _ = janela.read()
            if evento in (sg.WIN_CLOSED, 'Sair'):
                janela.close()
                return 'sair'
            if evento == 'Logout':
                janela.close()
                return 'logout'
            janela.close()
            return evento

    def _obter_botoes(self, perfil: str) -> list:
        """Retorna lista de botões conforme perfil."""
        if perfil == 'secretaria':
            return [
                'Gerenciar Alunos',       # RF01
                'Gerenciar Funcionários',  # RF03
                'Gerenciar Matrículas',    # RF02
                'Emitir Histórico',        # RF10
                'Relatório Turma',         # RF11
                'Relatório Professores'    # RF11
            ]
        elif perfil == 'coordenador':
            return [
                'Gerenciar Séries',        # RF04
                'Gerenciar Turmas',        # RF04
                'Gerenciar Matérias',       # RF04
                'Atribuir Professor'       # RF04
            ]
        elif perfil == 'professor':
            return [
                'Registrar Notas',         # RF05
                'Registrar Frequência',    # RF06
                'Editar Frequência'        # RF06
            ]
        elif perfil == 'aluno':
            return [
                'Consultar Boletim',       # RF09
                'Consultar Histórico'      # RF09
            ]
        return []
