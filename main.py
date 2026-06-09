import sys
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QProgressBar, QDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPalette, QLinearGradient, QBrush, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QRect
from medidor_circular import MedidorCircular
from tela_inform import TelaInfoSistema


class MainWindow(QMainWindow):  # define estrutura da janela
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elestroposto Fluvial")

        # travando o tamanho da janela principal
        self.setGeometry(300, 220, 900, 500)

        # fundo
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

        # logo
        logo_label = QLabel()

        #procura o diretório do arquivo python
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))

        #procura o nome da imagem
        caminho = os.path.join(diretorio_atual, "imagens", "logo_eletroposto.png")

        
        # --- ADICIONE ESTAS DUAS LINHAS PARA TESTAR ---
        print(f"Caminho que o Python montou: {caminho}")
        print(f"O Windows encontrou o arquivo? {os.path.exists(caminho)}")
        # ---------------------------------------------
        
        pixmap = QPixmap(caminho)
    
        pixmap = pixmap.scaled(420, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)

        # adicionar a logo ao layout
        layout.addWidget(logo_label, alignment=Qt.AlignHCenter | Qt.AlignTop)
        

        # adicionar os indicadores
        indicadores_layout = QHBoxLayout()
        layout.addLayout(indicadores_layout)

        # centralizando os indicadores horizontalmente
        indicadores_layout.setAlignment(Qt.AlignCenter)

        # corrente
        self.corrente = MedidorCircular("CORRENTE (A)", "150", "A")
        indicadores_layout.addWidget(self.corrente)

        # voltagem
        self.voltagem = MedidorCircular("TENSÃO (V)", "380", "V")
        indicadores_layout.addWidget(self.voltagem)

        # sOC (Bateria)
        self.soc = MedidorCircular("SOC (CARGA)", "85", "%", True)
        indicadores_layout.addWidget(self.soc)

        # adicionando um espaço entre eles
        indicadores_layout.setSpacing(50)

        #layout botões
        botao_layout = QHBoxLayout()
        botao_layout.setSpacing(20)
        layout.addLayout(botao_layout)

        #criando botões
        btn_inicio = self.criar_botao("INÍCIO")
        btn_config = self.criar_botao("CONFIGURAÇÕES DE CARGA") 
        btn_info = self.criar_botao("INFO. DO SISTEMA")

        #adicionando os botões ao layout

        botao_layout.addWidget(btn_inicio)
        botao_layout.addWidget(btn_config)
        botao_layout.addWidget(btn_info)

        btn_info.clicked.connect(self.acao_info)

        #adicionando botao de parar carregamento + rodape
        rodape_layout = QHBoxLayout()
        rodape_layout.setContentsMargins(50,20,50,20)
        layout.addLayout(rodape_layout)

        barra_layout = QVBoxLayout()

        self.barra_progresso = QProgressBar()
        self.barra_progresso.setValue(85) # Mesmo valor do SOC
        self.barra_progresso.setTextVisible(False) # Esconde a porcentagem de dentro da barra
        self.barra_progresso.setFixedHeight(15) # Deixa ela bem fininha
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
        
        # O texto de baixo da barra
        label_tempo = QLabel("TEMPO RESTANTE: 04M")
        label_tempo.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        label_tempo.setAlignment(Qt.AlignRight) # Alinha o texto à direita da barra
        
        # Adiciona a barra e o texto no seu mini-layout
        barra_layout.addWidget(self.barra_progresso)
        barra_layout.addWidget(label_tempo)
        
        # Adiciona esse mini-layout no lado esquerdo do rodapé
        rodape_layout.addLayout(barra_layout)
        
        # 2. Empurra o botão lá pra direita
        rodape_layout.addStretch()

        # 3. Adicionando o Botão Vermelho
        btn_carregar = self.criar_botao1("PARAR CARREGAMENTO")
        # Definimos uma largura fixa para ele não esticar
        btn_carregar.setFixedWidth(300) 
        rodape_layout.addWidget(btn_carregar)



        layout.addStretch()

    def criar_botao(self, texto):
        botao = QPushButton(texto) #criação do objeto botão

        botao.setMinimumHeight(50)

        #QSS para criar efeito neon
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
    
    def criar_botao1(self, texto): # Mudei o nome para ficar mais claro
            
            botao1 = QPushButton(texto)
            botao1.setMinimumHeight(60) # Deixei um pouquinho mais alto que os azuis

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

    def acao_info (self):
        tela = TelaInfoSistema(self)

        tela.exec()
        
    
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
