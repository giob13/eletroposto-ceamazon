from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog
from PyQt5.QtCore import Qt


class TelaInfoSistema(QDialog): 
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Informações do Sistema")
        self.setFixedSize(400, 350)

        # Definindo fundo

        self.setStyleSheet("background-color: #a5d2fa")

        # Organizando os widgets de forma vertical
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Formatando dos textos

        titulo = QLabel("INFORMAÇÕES DO ELETROPOSTO")  # mudo pra sistema?
        titulo.setStyleSheet(
            "color: #202931; font-size: 16px; font-weight: bold;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Adicionando as informações
        info_texto = """
        - Modelo: Eletroposto Fluvial 
        - Versão do Firmware:
        - Ip de Rede:
        - Status do Servidor: Conectado
        - Temperatura Interna:
        - Tensão Nominal:
        - última Manuntenção:

        """

        label_info = QLabel(info_texto)
        label_info.setStyleSheet("color: black; font-size: 14px;")
        layout.addWidget(label_info)

        layout.addStretch()

        # Botão para fechar janela pop-up
        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setMaximumHeight(40)
        btn_fechar.setStyleSheet("""

        QPushButton {
            background-color: rgba(10,30,80,150);
            color: white;
            font-size: 12px;
            font-weight: bold;
            border: 2px solid #0078d7;
            border-radius: 5px;           
                                 }
        
        QPushButton:hover {
            bacground-color: rgba(0,120,215,100);
                                 
                                 }
        """)

        # Conectar o clique a função nativa de fechar janela
        btn_fechar.clicked.connect(self.close)
        layout.addWidget(btn_fechar)
