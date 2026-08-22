import sys
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QProgressBar, QDialog
from PyQt5.QtGui import QPixmap, QColor, QPalette, QLinearGradient, QBrush, QFont, QFontMetrics
from PyQt5.QtCore import Qt
from elementos_graficos import MedidorCircular
from infor import TelaInfoSistema
from conf import Configuracoes
from soc import monitoramento_soc


class MainWindow(QMainWindow):  # Define estrutura da janela
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elestroposto Fluvial")

        # travando o tamanho da janela principal
        self.setGeometry(300, 220, 900, 500)

        # Fundo
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.setContentsMargins(15, 15, 15, 15)

        # gradiente - direção do  degradê
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor('#325fad'))
        gradient.setColorAt(0.5, QColor('#1d3462'))
        gradient.setColorAt(1.0, QColor('#0d1c39'))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        widget.setPalette(palette)

        # Logo
        logo_label = QLabel()

        # Procura o diretório do arquivo python
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))

        # Procura o nome da imagem
        caminho = os.path.join(
            diretorio_atual, "imagens", "logo_eletroposto.png")

        # Testar o caminho da imagem
        print(f"Caminho que o Python montou: {caminho}")
        print(f"O Windows encontrou o arquivo? {os.path.exists(caminho)}")

        pixmap = QPixmap(caminho)

        pixmap = pixmap.scaled(
            420, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)

        layout.addWidget(logo_label, alignment=Qt.AlignHCenter |
                         Qt.AlignTop)  # Adicionar a logo ao layout

        # Indicadores
        indicadores_layout = QHBoxLayout()
        layout.addLayout(indicadores_layout)
        # Centralizando os indicadores horizontalmente
        indicadores_layout.setAlignment(Qt.AlignCenter)

        # Medidores com variáveis dinâmicas 
        #Atualizar se houver mudança de configuração
        # corrente
        self.corrente = MedidorCircular("CORRENTE (A)", "150", "A")
        indicadores_layout.addWidget(self.corrente)

        # voltagem
        self.voltagem = MedidorCircular("TENSÃO (V)", "360", "V")
        indicadores_layout.addWidget(self.voltagem)

        # sOC (Bateria) - verificar qual carga o veículo está e mostrar
        self.soc = MedidorCircular("SOC (CARGA)", "0", "%", True)
        indicadores_layout.addWidget(self.soc)

        indicadores_layout.setSpacing(50)  # Adicionando um espaço entre eles

        #Monitoramento
        self.sinais_soc = monitoramento_soc()

        self.sinais_soc.carga_atualizada.connect(self.atualizar_soc)
        self.sinais_soc.status_alterado.connect(self.atualizar_status)
        self.sinais_soc.carregamento_concluido.connect(self.finalizar_carregamento)

        # Layout botões
        botao_layout = QHBoxLayout()
        botao_layout.setSpacing(20)
        layout.addLayout(botao_layout)

        # Criando botões
        self.btn_inicio = self.criar_botao("INÍCIO")
        self.btn_config = self.criar_botao("CONFIGURAÇÕES DE CARGA")
        self.btn_info = self.criar_botao("INFO. DO SISTEMA")

        # LIGANDO OS BOTÕES DE INÍCIO E PARADA AO MOTOR SOC:
        self.btn_inicio.clicked.connect(self.sinais_soc.iniciar_carregamento)
                

        # Adicionando os botões ao layout
        botao_layout.addWidget(self.btn_inicio)
        botao_layout.addWidget(self.btn_config)
        botao_layout.addWidget(self.btn_info)

        self.btn_info.clicked.connect(self.acao_info)
        self.btn_config.clicked.connect(self.acao_config)

        # Rodapé - adicionando botão de parar carregamento
        rodape_layout = QHBoxLayout()
        rodape_layout.setContentsMargins(50, 20, 50, 20)
        layout.addLayout(rodape_layout)

        barra_layout = QVBoxLayout()

        self.barra_progresso = QProgressBar()
        self.barra_progresso.setValue(0)  # Mesmo valor do SOC
        # Esconde a porcentagem de dentro da barra
        self.barra_progresso.setTextVisible(False)
        self.barra_progresso.setFixedHeight(15)  # Deixa ela bem fininha
        self.barra_progresso.setFixedWidth(350)

        # QSS para a barra ficar azul clara com fundo escuro
        self.barra_progresso.setStyleSheet("""
            QProgressBar {
                background-color: #1a2f5a;
                border: none;
                border-radius: 10px;
            }
            QProgressBar::chunk {
                background-color: #00e5ff;
                border-radius: 10px;
            }
        """)

        # Legenda da barra de carregamento
        label_tempo = QLabel("TEMPO RESTANTE") #CALCULAR O TEMPO TOTAL DE CARREGAMENTO 
        label_tempo.setStyleSheet(
            "color: white; font-weight: bold; font-size: 16px;")
        # Alinha o texto à direita da barra
        label_tempo.setAlignment(Qt.AlignRight)

        # Adiciona a barra e o texto no seu mini-layout
        barra_layout.addWidget(self.barra_progresso)
        barra_layout.addWidget(label_tempo)

        # Adiciona esse mini-layout no lado esquerdo do rodapé
        rodape_layout.addLayout(barra_layout)

        # Empurra o botão lá pra direita
        rodape_layout.addStretch()

        # Adicionando o Botão Vermelho
        self.btn_carregar = self.criar_botao1("PARAR CARREGAMENTO")
        # Definimos uma largura fixa para ele não esticar
        self.btn_carregar.setFixedWidth(300)
        rodape_layout.addWidget(self.btn_carregar)

        #Sinal do botão de parar carregamento
        self.btn_carregar.clicked.connect(self.acao_botao_vermelho)

        layout.addStretch()


    def criar_botao(self, texto):
        botao = QPushButton(texto)  # criação do objeto botão

        botao.setMinimumHeight(50)

        # QSS para criar efeito neon
        estilo = """
                QPushButton {
                    background-color: rgba(11, 103, 187, 150); /* Fundo azul bem escuro e levemente transparente */
                    color: white;
                    font-family: Arial;
                    font-size: 16px;
                    font-weight: bold;
                    border: 2px solid #0078d7; /* Borda azul brilhante */
                    border-radius: 5px; /* Cantos levemente arredondados */
                    padding: 5px 25px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 120, 215, 100); /* Fica mais claro ao passar o mouse */
                    border: 2px solid #00aaff; /* Borda acende mais */
                }
                QPushButton:pressed {
                    background-color: rgba(0, 80, 150, 200); /* Fica escuro quando clica */
                }
            """
        botao.setStyleSheet(estilo)

        return botao

    def criar_botao1(self, texto):  # Mudei o nome para ficar mais claro

        botao1 = QPushButton(texto)
        # Deixei um pouquinho mais alto que os azuis
        botao1.setMinimumHeight(60)

        estilo1 = """
                QPushButton {
                    background-color: #e54d2e; /* Vermelho/Laranja Sólido */
                    color: white;
                    font-family: Arial;
                    font-size: 18px;
                    font-weight: bold;
                    border: 2px solid #ffffff; /* Borda Branca (6 letras F!) */
                    border-radius: 30px; /* Bem arredondado, como uma pílula */
                    padding: 5px 30px;
                }
                QPushButton:hover {
                    background-color: #f75c3d; /* Ligeiramente mais claro no hover */
                    border: 2px solid #ffcccc; 
                }
                QPushButton:pressed {
                    background-color: #c93b1d; /* Mais escuro no clique */
                }
            """
        botao1.setStyleSheet(estilo1)
        return botao1
    
    def acao_info(self):
        tela_info = TelaInfoSistema(self)

        tela_info.exec()

    def acao_config(self):
        tela_config = Configuracoes(self)
        
        if tela_config.exec() == QDialog.Accepted:
            #1. Coleta os dados novos
            dados_configurados = tela_config.obter_configuracoes()
            #2. Atualizar os dados (o erro está aqui, o caminho soc n está completo)
            self.sinais_soc.atualizar_configuracoes(dados_configurados)
            # 3. (Opcional) Você pode atualizar um texto no próprio main.py mostrando o novo limite
            print("Configurações salvas e enviadas com sucesso!")
        else: 
            print("O usuário fechou ou cancelou as configurações.")

    def acao_botao_vermelho(self):
        # Se o botão estiver como "Parar", ele corta a energia
        if self.btn_carregar.text() == "PARAR CARREGAMENTO":
            self.sinais_soc.parar_carregamento()
            self.btn_carregar.setText("FINALIZAR") # Transforma o botão
            self.btn_inicio.setEnabled(True)       # Libera o início novamente
            
        # Se já estiver parado/concluído e o texto for "Finalizar", ele limpa a tela
        elif self.btn_carregar.text() == "FINALIZAR":
            self.sinais_soc.resetar_sistema()
            self.btn_carregar.setText("PARAR CARREGAMENTO") # Volta ao original
            
            # (Opcional) Trava o botão vermelho até iniciarem uma nova carga
            # self.btn_carregar.setEnabled(False)

    def atualizar_soc(self, porcentagem):
        self.soc.atualizar_valor(porcentagem)
        self.barra_progresso.setValue(porcentagem)

    def atualizar_status (self, status):
        print(f"O Status mudou para: {status}")
        # Manda a palavra nova para o mostrador redondo!
        self.soc.atualizar_texto_status(status)
  

    def finalizar_carregamento(self):
        print("Carregamento concluído!")
        
        # Como o processo acabou com sucesso, o botão vira "FINALIZAR"
        self.btn_carregar.setText("FINALIZAR")
        self.btn_inicio.setEnabled(True) # Libera para um novo início
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
