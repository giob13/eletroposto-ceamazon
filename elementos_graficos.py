from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QRect

class MedidorCircular(QWidget):
    def __init__(self, titulo, valor, unidade, is_soc=False):
        super().__init__()
        self.setFixedSize(240, 240)

        self.titulo = titulo
        self.valor = int(valor)
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
                             Qt.AlignCenter, "CARREGANDO") #MUDAR AQUI PARA MOSTRAR O STATUS

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

        # CORREÇÃO 1: Adicionado o str() aqui
        largura_valor = fm_valor.width(str(self.valor)) 
        largura_unidade = fm_unidade.width(self.unidade)
        largura_total = largura_valor + largura_unidade + 2  # +2 é um pequeno espaço entre eles

        # calculando o ponto de partida 'X' para que fiquem no centro do círculo
        x_inicial = rect_externo.center().x() - (largura_total // 2)

        # 'Y' central. pegamos o meio do retângulo e somamos um pouco para ajustar visualmente
        y_central = rect_externo.center().y() + (fm_valor.height() // 3)

        if self.is_soc:
            y_central -= 10  # Sobe um pouco para não bater no "CARREGANDO"

        painter.setFont(fonte_valor)
        # Aqui você já tinha feito certo usando o str()!
        painter.drawText(x_inicial, y_central, str(self.valor))

        painter.setFont(fonte_unidade)
        painter.drawText(x_inicial + largura_valor + 2, y_central, self.unidade)

        painter.end()

    def atualizar_valor(self, novo_valor):
        # CORREÇÃO 2: Atualiza a variável correta e converte para int
        self.valor = int(novo_valor) 
        self.update() # Força o widget a se redesenhar com o novo número