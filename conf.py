from PyQt5.QtWidgets import QSpacerItem, QHBoxLayout, QSizePolicy, QVBoxLayout, QButtonGroup, QRadioButton, QLabel, QPushButton, QDialog, QSpinBox
from PyQt5.QtCore import Qt


class Configuracoes(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurações da Janela
        self.setWindowTitle("Configurações do Eletroposto")
        self.setFixedSize(400, 350)

        # Definindo fundo e estilo geral
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF; /* Fundo totalmente branco */
                color: #000000;            /* Texto preto */
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                color: #000000; /* Garante que os rótulos sejam pretos */
            }
            QSpinBox {
                background-color: #F5F5F5; /* Cinza bem clarinho para dar contraste */
                color: #000000;            /* Números pretos */
                border: 2px solid #A0A0A0; /* Borda cinza mais escura */
                border-radius: 5px;
                padding: 5px;
            }
            QRadioButton {
                color: #000000; /* Texto das bolinhas de seleção em preto */
            }
            QPushButton {
                background-color: #E0E0E0; /* Fundo cinza claro para parecer um botão */
                color: #000000;            /* Texto do botão em preto */
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D0D0D0; /* Escurece um pouco ao passar o mouse */
            }
        """)

        # Organizando os widgets de forma vertical
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Título da Janela
        titulo = QLabel("CONFIGURAÇÕES DE CARGA")
        titulo.setStyleSheet(
            "color: #000000; font-size: 16px; font-weight: bold;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # --------OPÇÕES DE CARREGAMENTO--------

        # Layout SOC
        layout_soc = QHBoxLayout()
        layout_soc.addWidget(QLabel("Limite de Carga (SOC):"))
        self.input_soc = QSpinBox()
        self.input_soc.setRange(50, 100)  # máximo e mínimo
        self.input_soc.setValue(80)
        self.input_soc.setSuffix(" %")
        self.input_soc.setFixedWidth(100)

        layout_soc.addWidget(self.input_soc)
        layout.addLayout(layout_soc)

        # Layout Corrente Máxima
        layout_corrente = QHBoxLayout()
        layout_corrente.addWidget(QLabel("Corrente Máxima:"))
        self.input_corrente = QSpinBox()
        self.input_corrente.setRange(10, 200)
        self.input_corrente.setValue(150)
        self.input_corrente.setSuffix(" A")
        self.input_corrente.setFixedWidth(100)

        layout_corrente.addWidget(self.input_corrente)
        layout.addLayout(layout_corrente)

        # Layout Modo de Operação
        layout_modo = QHBoxLayout()
        layout_modo.addWidget(QLabel("Modo de Operação:"))
        layout_radios = QHBoxLayout()
        self.radio_normal = QRadioButton("Normal")
        self.radio_rapido = QRadioButton("Rápido")
        self.radio_rapido.setChecked(True)

        self.grupo_modos = QButtonGroup(self)
        self.grupo_modos.addButton(self.radio_normal)
        self.grupo_modos.addButton(self.radio_rapido)

        layout_radios.addWidget(self.radio_normal)
        layout_radios.addWidget(self.radio_rapido)
        layout_modo.addLayout(layout_radios)
        layout.addLayout(layout_modo)

        # Espaçador
        layout.addSpacerItem(QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botão para salvar
        self.btn_salvar = QPushButton("SALVAR")
        self.btn_salvar.setMaximumHeight(40)
        self.btn_salvar.clicked.connect(self.accept)
        layout.addWidget(self.btn_salvar)

        # Botão para fechar
        self.btn_fechar = QPushButton("FECHAR")
        self.btn_fechar.setMaximumHeight(40)
        self.btn_fechar.clicked.connect(self.reject)
        layout.addWidget(self.btn_fechar)


# Bloco para testar a janela isoladamente
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    janela = Configuracoes()
    janela.show()
    sys.exit(app.exec_())
