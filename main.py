# main.py
# Ponto de entrada do Sistema de Gestão Escolar
# Orquestra fluxo MVC: View -> Controller específico -> Model/Cache
# Cada controller é atômico e responsável pelo seu próprio modelo.

from cache.cache_manager import CacheManager
from model.usuario import Usuario
from model.secretaria import Secretaria
from model.coordenador import Coordenador
from model.professor import Professor
from model.aluno import Aluno

# Controllers - um por modelo concreto
from controller.sistema_controller import SistemaController
from controller.professor_controller import ProfessorController
from controller.secretaria_controller import SecretariaController
from controller.coordenador_controller import CoordenadorController
from controller.aluno_controller import AlunoController
from controller.usuario_controller import UsuarioController
from controller.serie_controller import SerieController
from controller.turma_controller import TurmaController
from controller.materia_controller import MateriaController
from controller.matricula_controller import MatriculaController
from controller.nota_controller import NotaController
from controller.frequencia_controller import FrequenciaController
from controller.boletim_controller import BoletimController
from controller.historico_controller import HistoricoController

# Views
from view.tela_login import TelaLogin
from view.tela_menu import TelaMenu
from view.tela_aluno import TelaAluno
from view.tela_funcionario import TelaFuncionario
from view.tela_serie import TelaSerie
from view.tela_turma import TelaTurma
from view.tela_materia import TelaMateria
from view.tela_matricula import TelaMatricula
from view.tela_nota import TelaNota
from view.tela_frequencia import TelaFrequencia
from view.tela_boletim import TelaBoletim
from view.tela_historico import TelaHistorico


class SistemaEscolar:
    """Classe principal que orquestra o sistema MVC."""

    def __init__(self):
        # Controllers - instanciados individualmente (cada um atômico)
        self._sistema_ctrl = SistemaController()
        self._professor_ctrl = ProfessorController()
        self._secretaria_ctrl = SecretariaController()
        self._coordenador_ctrl = CoordenadorController()
        self._aluno_ctrl = AlunoController()
        self._usuario_ctrl = UsuarioController()
        self._serie_ctrl = SerieController()
        self._turma_ctrl = TurmaController()
        self._materia_ctrl = MateriaController()
        self._matricula_ctrl = MatriculaController()
        self._nota_ctrl = NotaController()
        self._frequencia_ctrl = FrequenciaController()
        self._boletim_ctrl = BoletimController()
        self._historico_ctrl = HistoricoController()

        # Views
        self._tela_login = TelaLogin()
        self._tela_menu = TelaMenu()
        self._tela_aluno = TelaAluno()
        self._tela_func = TelaFuncionario()
        self._tela_serie = TelaSerie()
        self._tela_turma = TelaTurma()
        self._tela_materia = TelaMateria()
        self._tela_matricula = TelaMatricula()
        self._tela_nota = TelaNota()
        self._tela_freq = TelaFrequencia()
        self._tela_boletim = TelaBoletim()
        self._tela_historico = TelaHistorico()

        self._criar_dados_iniciais()

    def _criar_dados_iniciais(self):
        """Cria usuários iniciais para teste do sistema."""
        cache = CacheManager()
        sec = Secretaria(nome="Maria Silva", cpf="111.111.111-11",
                         matricula_funcionario="SEC001", setor="Acadêmica")
        usr_sec = Usuario(login="secretaria", senha="123", perfil="secretaria")
        sec.usuario = usr_sec
        cache.adicionar_secretaria(sec)
        cache.adicionar_usuario(usr_sec)

        coord = Coordenador(nome="João Santos", cpf="222.222.222-22",
                            matricula_funcionario="COORD001", area="Pedagógica")
        usr_coord = Usuario(login="coordenador", senha="123", perfil="coordenador")
        coord.usuario = usr_coord
        cache.adicionar_coordenador(coord)
        cache.adicionar_usuario(usr_coord)

        prof = Professor(nome="Ana Oliveira", cpf="333.333.333-33",
                         matricula_funcionario="PROF001",
                         formacao="Matemática", titulacao="Mestre")
        usr_prof = Usuario(login="professor", senha="123", perfil="professor")
        prof.usuario = usr_prof
        cache.adicionar_professor(prof)
        cache.adicionar_usuario(usr_prof)

        aluno = Aluno(nome="Pedro Costa", cpf="444.444.444-44",
                      responsavel="Carlos Costa", telefone_responsavel="48999999999")
        usr_aluno = Usuario(login="aluno", senha="123", perfil="aluno")
        aluno.usuario = usr_aluno
        cache.adicionar_aluno(aluno)
        cache.adicionar_usuario(usr_aluno)

    def iniciar(self):
        """Inicia o sistema: loop de login -> menu."""
        while True:
            login, senha = self._tela_login.abrir()
            if login is None:
                break
            if self._sistema_ctrl.autenticar(login, senha):
                self._loop_menu()
            else:
                self._tela_login.exibir_erro_login()

    def _loop_menu(self):
        """Loop do menu principal conforme perfil logado."""
        perfil = self._sistema_ctrl.obter_perfil()
        pessoa = self._sistema_ctrl.pessoa_logada
        nome = pessoa.nome if pessoa else "Usuário"
        while True:
            opcao = self._tela_menu.abrir(perfil, nome)
            if opcao in ('sair', 'logout', None):
                self._sistema_ctrl.logout()
                return
            self._rotear_opcao(opcao)

    def _rotear_opcao(self, opcao: str):
        """Roteia a opção do menu para o fluxo correspondente."""
        rotas = {
            'Gerenciar Alunos': self._fluxo_alunos,
            'Gerenciar Funcionários': self._fluxo_funcionarios,
            'Gerenciar Matrículas': self._fluxo_matriculas,
            'Emitir Histórico': self._fluxo_emitir_historico,
            'Relatório Turma': self._fluxo_relatorio_turma,
            'Relatório Professores': self._fluxo_relatorio_professores,
            'Gerenciar Séries': self._fluxo_series,
            'Gerenciar Turmas': self._fluxo_turmas,
            'Gerenciar Matérias': self._fluxo_materias,
            'Atribuir Professor': self._fluxo_atribuir_professor,
            'Registrar Notas': self._fluxo_notas,
            'Registrar Frequência': self._fluxo_frequencia,
            'Editar Frequência': self._fluxo_editar_frequencia,
            'Consultar Boletim': self._fluxo_consultar_boletim,
            'Consultar Histórico': self._fluxo_consultar_historico,
        }
        fluxo = rotas.get(opcao)
        if fluxo:
            fluxo()

    # === FLUXOS SECRETARIA ===

    def _fluxo_alunos(self):
        """Gerenciamento de alunos via SecretariaController (RF01)."""
        secretaria = self._sistema_ctrl.pessoa_logada
        while True:
            opcao = self._tela_aluno.abrir_menu_aluno()
            if opcao == 'Voltar':
                return
            if opcao == 'Cadastrar Aluno':
                dados = self._tela_aluno.abrir_cadastro()
                if dados:
                    if self._secretaria_ctrl.cadastrar_aluno(secretaria, dados):
                        self._tela_aluno.exibir_sucesso('Aluno cadastrado com sucesso!')
                    else:
                        self._tela_aluno.exibir_erro('CPF já cadastrado ou erro no cadastro.')
            elif opcao == 'Editar Aluno':
                cpf = self._tela_aluno.abrir_consulta()
                if cpf:
                    aluno = self._secretaria_ctrl.consultar_aluno(cpf)
                    dados = self._tela_aluno.abrir_edicao(aluno)
                    if dados:
                        if self._secretaria_ctrl.editar_aluno(secretaria, cpf, dados):
                            self._tela_aluno.exibir_sucesso('Aluno atualizado!')
                        else:
                            self._tela_aluno.exibir_erro('Erro ao editar.')
            elif opcao == 'Consultar Aluno':
                cpf = self._tela_aluno.abrir_consulta()
                if cpf:
                    aluno = self._secretaria_ctrl.consultar_aluno(cpf)
                    self._tela_aluno.exibir_dados_aluno(aluno)
            elif opcao == 'Listar Alunos':
                self._tela_aluno.abrir_listagem(self._secretaria_ctrl.listar_alunos())

    def _fluxo_funcionarios(self):
        """Gerenciamento de funcionários via SecretariaController (RF03)."""
        secretaria = self._sistema_ctrl.pessoa_logada
        while True:
            opcao = self._tela_func.abrir_menu()
            if opcao == 'Voltar':
                return
            if opcao == 'Cadastrar Professor':
                dados = self._tela_func.abrir_cadastro_professor()
                if dados:
                    if self._secretaria_ctrl.cadastrar_funcionario(secretaria, dados):
                        self._tela_func.exibir_sucesso('Professor cadastrado!')
                    else:
                        self._tela_func.exibir_erro('Matrícula já existente.')
            elif opcao == 'Cadastrar Secretária':
                dados = self._tela_func.abrir_cadastro_secretaria()
                if dados:
                    if self._secretaria_ctrl.cadastrar_funcionario(secretaria, dados):
                        self._tela_func.exibir_sucesso('Secretária cadastrada!')
                    else:
                        self._tela_func.exibir_erro('Matrícula já existente.')
            elif opcao == 'Consultar Funcionário':
                mat = self._tela_func.abrir_consulta()
                if mat:
                    func = self._secretaria_ctrl.consultar_funcionario(mat)
                    self._tela_func.exibir_dados(func)
            elif opcao == 'Listar Professores':
                self._tela_func.abrir_listagem(self._professor_ctrl.listar_professores())

    def _fluxo_matriculas(self):
        """Gerenciamento de matrículas via SecretariaController (RF02)."""
        secretaria = self._sistema_ctrl.pessoa_logada
        while True:
            opcao = self._tela_matricula.abrir_menu()
            if opcao == 'Voltar':
                return
            if opcao == 'Efetuar Matrícula':
                alunos = self._aluno_ctrl.listar_alunos()
                turmas = self._turma_ctrl.listar()
                cpf, cod_turma = self._tela_matricula.abrir_efetuar(alunos, turmas)
                if cpf and cod_turma:
                    mat = self._secretaria_ctrl.efetuar_matricula(secretaria, cpf, cod_turma)
                    if mat:
                        self._tela_matricula.exibir_sucesso(f'Matrícula {mat.codigo} efetuada!')
                    else:
                        self._tela_matricula.exibir_erro('Turma cheia (RN05) ou dados inválidos.')
            elif opcao == 'Cancelar Matrícula':
                mats = self._matricula_ctrl.listar()
                cod = self._tela_matricula.abrir_cancelar(mats)
                if cod:
                    if self._secretaria_ctrl.cancelar_matricula(secretaria, cod):
                        self._tela_matricula.exibir_sucesso('Matrícula cancelada.')
            elif opcao == 'Transferir Matrícula':
                mats = self._matricula_ctrl.listar()
                turmas = self._turma_ctrl.listar()
                cod_mat, cod_turma = self._tela_matricula.abrir_transferir(mats, turmas)
                if cod_mat and cod_turma:
                    if self._secretaria_ctrl.transferir_matricula(secretaria, cod_mat, cod_turma):
                        self._tela_matricula.exibir_sucesso('Matrícula transferida!')
                    else:
                        self._tela_matricula.exibir_erro('Turma destino cheia (RN05).')
            elif opcao == 'Listar Matrículas':
                self._tela_matricula.abrir_listagem(self._matricula_ctrl.listar())

    def _fluxo_emitir_historico(self):
        """Emissão de histórico escolar via SecretariaController (RF10)."""
        secretaria = self._sistema_ctrl.pessoa_logada
        cpf = self._tela_historico.solicitar_cpf()
        if cpf:
            hist = self._secretaria_ctrl.emitir_historico(secretaria, cpf)
            aluno = self._secretaria_ctrl.consultar_aluno(cpf)
            nome = aluno.nome if aluno else ''
            self._tela_historico.exibir_historico(hist, nome)

    def _fluxo_relatorio_turma(self):
        """Relatório de alunos por turma via SecretariaController (RF11)."""
        import PySimpleGUI as sg
        secretaria = self._sistema_ctrl.pessoa_logada
        turmas = self._turma_ctrl.listar()
        if not turmas:
            sg.popup('Nenhuma turma cadastrada.')
            return
        lt = [f"{t.codigo} - {t.nome}" for t in turmas]
        cod = sg.popup_get_text('Código da turma:', default_text=lt[0].split(' - ')[0] if lt else '')
        if cod:
            rel = self._secretaria_ctrl.gerar_relatorio_turma(secretaria, cod.strip())
            if rel:
                dados = [[r['aluno'], r['cpf'], r['matricula'], r['status']] for r in rel]
                layout = [
                    [sg.Table(values=dados, headings=['Aluno', 'CPF', 'Matrícula', 'Status'],
                              auto_size_columns=True)],
                    [sg.Button('Fechar')]
                ]
                j = sg.Window('Relatório Turma', layout)
                j.read()
                j.close()
            else:
                sg.popup('Nenhum aluno nesta turma.')

    def _fluxo_relatorio_professores(self):
        """Relatório de professores por série via SecretariaController (RF11)."""
        import PySimpleGUI as sg
        secretaria = self._sistema_ctrl.pessoa_logada
        series = self._serie_ctrl.listar()
        if not series:
            sg.popup('Nenhuma série cadastrada.')
            return
        cod = sg.popup_get_text('Código da série:')
        if cod:
            rel = self._secretaria_ctrl.gerar_relatorio_professores(secretaria, cod.strip())
            if rel:
                dados = [[r['professor'], r['matricula'], r['materia'], r['turma']] for r in rel]
                layout = [
                    [sg.Table(values=dados, headings=['Professor', 'Matrícula', 'Matéria', 'Turma'],
                              auto_size_columns=True)],
                    [sg.Button('Fechar')]
                ]
                j = sg.Window('Relatório Professores', layout)
                j.read()
                j.close()
            else:
                sg.popup('Nenhum professor alocado nesta série.')

    # === FLUXOS COORDENADOR ===

    def _fluxo_series(self):
        """Cadastro de séries via CoordenadorController (RF04)."""
        coordenador = self._sistema_ctrl.pessoa_logada
        dados = self._tela_serie.abrir_cadastro()
        if dados:
            serie = self._coordenador_ctrl.cadastrar_serie(coordenador, dados)
            if serie:
                self._tela_serie.exibir_sucesso(f'Série {serie.nome} cadastrada!')
            else:
                self._tela_serie.exibir_erro('Código já existe ou permissão negada.')

    def _fluxo_turmas(self):
        """Cadastro de turmas via CoordenadorController (RF04, RN05)."""
        coordenador = self._sistema_ctrl.pessoa_logada
        series = self._serie_ctrl.listar()
        dados = self._tela_turma.abrir_cadastro(series)
        if dados:
            turma = self._coordenador_ctrl.cadastrar_turma(coordenador, dados)
            if turma:
                self._tela_turma.exibir_sucesso(
                    f'Turma {turma.nome} cadastrada com capacidade {turma.capacidade_maxima}!')
            else:
                self._tela_turma.exibir_erro(
                    'Erro: série não encontrada ou capacidade não informada (RN05).')

    def _fluxo_materias(self):
        """Cadastro de matérias via CoordenadorController (RF04)."""
        coordenador = self._sistema_ctrl.pessoa_logada
        dados = self._tela_materia.abrir_cadastro()
        if dados:
            mat = self._coordenador_ctrl.cadastrar_materia(coordenador, dados)
            if mat:
                self._tela_materia.exibir_sucesso(f'Matéria {mat.nome} cadastrada!')
            else:
                self._tela_materia.exibir_erro('Código já existe.')

    def _fluxo_atribuir_professor(self):
        """Atribuição de professor a matéria/turma via CoordenadorController (RF04)."""
        import PySimpleGUI as sg
        coordenador = self._sistema_ctrl.pessoa_logada
        profs = self._professor_ctrl.listar_professores()
        mats = self._materia_ctrl.listar()
        turmas = self._turma_ctrl.listar()
        if not profs or not mats or not turmas:
            sg.popup('Cadastre professores, matérias e turmas primeiro.')
            return
        lp = [f"{p.matricula_funcionario} - {p.nome}" for p in profs]
        lm = [f"{m.codigo} - {m.nome}" for m in mats]
        lt = [f"{t.codigo} - {t.nome}" for t in turmas]
        layout = [
            [sg.Text('Atribuir Professor a Matéria/Turma (RF04)')],
            [sg.Text('Professor:'), sg.Combo(lp, key='-PROF-', size=(30, 1))],
            [sg.Text('Matéria:'), sg.Combo(lm, key='-MAT-', size=(30, 1))],
            [sg.Text('Turma:'), sg.Combo(lt, key='-TURMA-', size=(30, 1))],
            [sg.Button('Atribuir'), sg.Button('Cancelar')]
        ]
        j = sg.Window('Atribuir Professor', layout)
        e, v = j.read()
        j.close()
        if e == 'Atribuir' and v['-PROF-'] and v['-MAT-'] and v['-TURMA-']:
            mp = v['-PROF-'].split(' - ')[0]
            cm = v['-MAT-'].split(' - ')[0]
            ct = v['-TURMA-'].split(' - ')[0]
            if self._coordenador_ctrl.atribuir_professor_materia(coordenador, mp, cm, ct):
                sg.popup('Professor atribuído com sucesso!')
            else:
                sg.popup_error('Erro na atribuição.')

    # === FLUXOS PROFESSOR ===

    def _fluxo_notas(self):
        """Registro de notas via ProfessorController (RF05, RN06)."""
        professor = self._sistema_ctrl.pessoa_logada
        matriculas = self._matricula_ctrl.listar()
        materias = self._materia_ctrl.listar()
        dados = self._tela_nota.abrir_registro(matriculas, materias)
        if dados:
            ok = self._professor_ctrl.registrar_nota(
                professor,
                dados['cod_matricula'], dados['cod_materia'],
                dados['bimestre'], dados['valor']
            )
            if ok:
                self._tela_nota.exibir_sucesso('Nota registrada com sucesso!')
            else:
                self._tela_nota.exibir_erro('Erro: nota inválida (RN06) ou matrícula/matéria não encontrada.')

    def _fluxo_frequencia(self):
        """Registro de frequência via ProfessorController (RF06)."""
        professor = self._sistema_ctrl.pessoa_logada
        matriculas = self._matricula_ctrl.listar()
        materias = self._materia_ctrl.listar()
        dados = self._tela_freq.abrir_registro(matriculas, materias)
        if dados:
            ok = self._professor_ctrl.registrar_frequencia(
                professor,
                dados['cod_matricula'], dados['cod_materia'],
                dados['data_aula'], dados['presente']
            )
            if ok:
                tipo = 'Presença' if dados['presente'] else 'Falta'
                self._tela_freq.exibir_sucesso(f'{tipo} registrada com sucesso!')
            else:
                self._tela_freq.exibir_erro('Erro ao registrar frequência.')

    def _fluxo_editar_frequencia(self):
        """Edição de frequência via ProfessorController (RF06)."""
        professor = self._sistema_ctrl.pessoa_logada
        matriculas = self._matricula_ctrl.listar()
        materias = self._materia_ctrl.listar()
        dados = self._tela_freq.abrir_edicao(matriculas, materias)
        if dados:
            ok = self._professor_ctrl.editar_frequencia(
                professor,
                dados['cod_matricula'], dados['cod_materia'],
                dados['data_aula'], dados['presente']
            )
            if ok:
                self._tela_freq.exibir_sucesso('Frequência editada com sucesso!')
            else:
                self._tela_freq.exibir_erro('Registro não encontrado ou data inválida (RF06).')

    # === FLUXOS ALUNO ===

    def _fluxo_consultar_boletim(self):
        """Consulta de boletim via AlunoController e BoletimController (RF09, RF07, RF08)."""
        aluno = self._sistema_ctrl.pessoa_logada
        if not aluno or not aluno.matriculas:
            self._tela_boletim.exibir_erro('Nenhuma matrícula encontrada.')
            return
        cod = self._tela_boletim.abrir_selecao(aluno.matriculas)
        if cod:
            matricula = self._matricula_ctrl.buscar(cod)
            if matricula and matricula.boletim:
                boletim = self._boletim_ctrl.gerar(matricula.boletim, matricula.frequencias)
                self._tela_boletim.exibir_boletim(boletim)

    def _fluxo_consultar_historico(self):
        """Consulta de histórico via AlunoController (RF09)."""
        aluno = self._sistema_ctrl.pessoa_logada
        hist = self._aluno_ctrl.consultar_historico(aluno)
        nome = aluno.nome if aluno else ''
        self._tela_historico.exibir_historico(hist, nome)


# === Ponto de entrada ===
if __name__ == "__main__":
    sistema = SistemaEscolar()
    sistema.iniciar()
