import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QProgressBar
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPalette, QLinearGradient, QBrush, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QRect

#teste de brach

print("hello")

class MedidorCircular(QWidget):
    def __init__(self, titulo, valor, unidade, is_soc=False):
        super().__init__()
        self.setFixedSize(240, 240)

        self.titulo = titulo
        self.valor = valor
        self.unidade = unidade
        self.is_soc = is_soc

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # definindo áreas
        # área para o arco grosso (ciano) - deixamos espaço no topo para o título
        rect_externo = QRect(20, 50, 180, 180)

        # área para o arco fino (branco)
        margem_interna = 10
        rect_interno = QRect(rect_externo.x() + margem_interna,
                             rect_externo.y() + margem_interna,
                             rect_externo.width() - (margem_interna * 2),
                             rect_externo.height() - (margem_interna * 2))

        # ângulos dos arcos
        angulo_inicial = 135 * 16  # começa a desenhar no canto superior esquerdo
        # o arco percorre 270 graus (3/4 de um círculo)
        angulo_tamanho = 270 * 16

        # desenhando os arcos

        # arco externo (grosso e ciano)
        caneta_externa = QPen(QColor('#51ebf5'))  # Ciano brilhante
        caneta_externa.setWidth(8)
        caneta_externa.setCapStyle(Qt.RoundCap)  # pontas redondas
        painter.setPen(caneta_externa)
        painter.drawArc(rect_externo, angulo_inicial, angulo_tamanho)

        # arco interno (Fino e claro)
        caneta_interna = QPen(QColor('#ccffff'))  # ciano muito clarinho/branco
        caneta_interna.setWidth(2)
        caneta_interna.setCapStyle(Qt.RoundCap)
        painter.setPen(caneta_interna)
        painter.drawArc(rect_interno, angulo_inicial, angulo_tamanho)

        # medidor do carregamento => try-except é usado para tratar de exceções
        if self.is_soc:
            try:  # transforma o valor da carga em string
                porcentagem = int(self.valor)
            except:
                porcentagem = 0
            # calcula o tamanho do arco verde: (270 graus * 85) *16
            angulo_progresso = int((270*(porcentagem/100.0))*16)
            caneta_progresso = QPen(QColor('#a5ff00'))
            caneta_progresso.setWidth(6)
            caneta_progresso.setCapStyle(Qt.RoundCap)
            painter.setPen(caneta_progresso)
            painter.drawArc(rect_interno, angulo_inicial, angulo_progresso)

            # texto
            painter.setPen(QColor('white'))
            fonte_pequena = QFont("Arial", 8, QFont.Bold)
            painter.setFont(fonte_pequena)
            y_carregando = rect_externo.center().y() + 30  # Joga pra baixo do centro
            painter.drawText(QRect(rect_externo.x(), y_carregando, rect_externo.width(), 20),
                             Qt.AlignCenter, "CARREGANDO")

        # texto
        painter.setPen(QPen(Qt.white))

        # título no topo (ex: "CORRENTE (A)")
        fonte_titulo = QFont("Arial", 14, QFont.Bold)
        painter.setFont(fonte_titulo)
        painter.drawText(QRect(0, 20, self.width(), 30),
                         Qt.AlignHCenter, self.titulo)

        # valor e unidade no centro (tamanhos diferentes!)
        fonte_valor = QFont("Arial", 32, QFont.Bold)
        fonte_unidade = QFont("Arial", 16, QFont.Bold)

        # precisamos medir o tamanho dos textos para poder centralizá-los juntos
        fm_valor = QFontMetrics(fonte_valor)
        fm_unidade = QFontMetrics(fonte_unidade)

        largura_valor = fm_valor.width(self.valor)
        largura_unidade = fm_unidade.width(self.unidade)
        largura_total = largura_valor + largura_unidade + \
            2  # +2 é um pequeno espaço entre eles

        # calculando o ponto de partida 'X' para que fiquem no centro do círculo
        x_inicial = rect_externo.center().x() - (largura_total // 2)

        # 'Y' central. pegamos o meio do retângulo e somamos um pouco para ajustar visualmente
        y_central = rect_externo.center().y() + (fm_valor.height() // 3)

        if self.is_soc:
            y_central -= 10  # Sobe um pouco para não bater no "CARREGANDO"

        painter.setFont(fonte_valor)
        painter.drawText(x_inicial, y_central, self.valor)

        painter.setFont(fonte_unidade)
        painter.drawText(x_inicial + largura_valor +
                         2, y_central, self.unidade)

        painter.end()


class MainWindow(QMainWindow):  # define estrutura da janela
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elestroposto Marítimo")

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

        pixmap = QPixmap(
            "C:/Users/giova/Documents/CEAMAZON - PIBIC/códigos/testes_layout/eletroposto.mod.png")
        pixmap = pixmap.scaled(450, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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

    
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
