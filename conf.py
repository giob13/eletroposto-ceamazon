import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QButtonGroup,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
)


class Configuracoes(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurações da Janela
        self.setWindowTitle("Configurações de Carga")
        self.setFixedSize(400, 450)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # ==========================================
        # 1. LAYOUT PRINCIPAL (SEM MARGENS)
        # ==========================================
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ==========================================
        # 2. BARRA SUPERIOR (Teal)
        # ==========================================
        self.barra_sup = QFrame()
        self.barra_sup.setFixedHeight(40)
        self.barra_sup.setStyleSheet("""
            QFrame {
                background-color: #236B74; /* Cor Teal */
            }
        """)

        layout_barra = QHBoxLayout(self.barra_sup)
        layout_barra.setContentsMargins(15, 0, 15, 0)

        titulo_barra = QLabel("CONFIGURAÇÕES DO ELETROPOSTO")
        titulo_barra.setStyleSheet(
            "color: white; font-weight: bold; font-family: Arial; font-size:"
            " 13px; background: transparent;"
        )
        layout_barra.addWidget(
            titulo_barra, alignment=Qt.AlignLeft | Qt.AlignVCenter
        )

        # Adiciona a barra no topo da janela
        layout_principal.addWidget(self.barra_sup)

        # ==========================================
        # 3. ÁREA DE CONTEÚDO (Fundo Azul Escuro)
        # ==========================================
        self.area_conteudo = QFrame()
        self.area_conteudo.setStyleSheet("""
            QFrame {
                background-color: #102135; /* Fundo principal azul escuro */
            }
            QLabel {
                background-color: transparent; 
                color: white; 
                font-family: Arial;
                font-weight: bold;
                font-size: 13px;
            }
            QSpinBox {
                background-color: #1B2C42; /* Azul um pouco mais claro que o fundo */
                color: white;            /* Números em branco */
                border: 1px solid #2A4365;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QRadioButton {
                color: white; /* AJUSTADO: Texto das bolinhas em branco para aparecer no fundo escuro */
                font-weight: bold;
                background: transparent;
            }
            QPushButton {
                background-color: rgba(10,30,80,150); 
                color: white;
                font-size: 12px; 
                font-weight: bold; 
                border: 2px solid #0078d7; 
                border-radius: 5px;          
            }
            QPushButton:hover { 
                background-color: rgba(0,120,215,100); 
            }
        """)

        # Layout EXCLUSIVO da área de conteúdo
        layout_conteudo = QVBoxLayout(self.area_conteudo)
        layout_conteudo.setContentsMargins(30, 30, 30, 30)
        layout_conteudo.setSpacing(20)

        # ==========================================
        # 4. A LOGO COMO MARCA D'ÁGUA (FUNDO)
        # ==========================================
        self.fundo_eletroposto = QLabel(self.area_conteudo)
        self.fundo_eletroposto.lower()  # Envia a logo para trás de tudo

        diretorio = os.path.dirname(os.path.abspath(__file__))
        caminho_fundo = os.path.join(
            diretorio, "imagens", "fundo_eletroposto.png"
        )

        if os.path.exists(caminho_fundo):
            pixmap_fundo = QPixmap(caminho_fundo)
            pixmap_fundo = pixmap_fundo.scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.fundo_eletroposto.setPixmap(pixmap_fundo)
            # Centralizando a imagem no meio da área azul (X=75, Y=60)
            self.fundo_eletroposto.setGeometry(75, 60, 250, 250)

        # ==========================================
        # 5. CONTROLES DO FORMULÁRIO
        # ==========================================

        # --- Limite de Carga (SOC) ---
        layout_soc = QHBoxLayout()
        layout_soc.addWidget(QLabel("Limite de Carga (SOC):"))
        self.input_soc = QSpinBox()
        self.input_soc.setRange(50, 100)
        self.input_soc.setValue(80)
        self.input_soc.setSuffix(" %")
        self.input_soc.setFixedWidth(100)
        layout_soc.addWidget(self.input_soc)
        layout_conteudo.addLayout(layout_soc)  # Adiciona no layout_conteudo!

        # --- Corrente Máxima ---
        layout_corrente = QHBoxLayout()
        layout_corrente.addWidget(QLabel("Corrente Máxima:"))
        self.input_corrente = QSpinBox()
        self.input_corrente.setRange(10, 200)
        self.input_corrente.setValue(150)
        self.input_corrente.setSuffix(" A")
        self.input_corrente.setFixedWidth(100)
        layout_corrente.addWidget(self.input_corrente)
        layout_conteudo.addLayout(layout_corrente)

        # --- Modo de Operação ---
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
        layout_conteudo.addLayout(layout_modo)

        # Espaçador (Empurra os botões de Salvar e Fechar para o fim da tela)
        layout_conteudo.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
            )
        )

        # --- Botão Salvar ---
        self.btn_salvar = QPushButton("SALVAR")
        self.btn_salvar.setFixedHeight(40)
        self.btn_salvar.clicked.connect(self.accept)
        layout_conteudo.addWidget(self.btn_salvar)

        # --- Botão Fechar ---
        self.btn_fechar = QPushButton("FECHAR")
        self.btn_fechar.setFixedHeight(40)
        self.btn_fechar.clicked.connect(self.reject)
        layout_conteudo.addWidget(self.btn_fechar)

        # Finaliza adicionando a área de conteúdo montada à janela principal
        layout_principal.addWidget(self.area_conteudo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Configuracoes()
    janela.show()
    sys.exit(app.exec_())