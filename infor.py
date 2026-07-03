import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class TelaInfoSistema(QDialog): 
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurações da Janela
        # Usamos FramelessWindowHint para remover a barra branca padrão do Windows se quiser o visual 100% customizado.
        # self.setWindowFlags(Qt.FramelessWindowHint) 
        self.setWindowTitle("Informações do Sistema")
        self.setFixedSize(400, 450) # Aumentei um pouco a altura para caber tudo

        self.setAttribute(Qt.WA_StyledBackground, True)

        # 1. LAYOUT PRINCIPAL (SEM MARGENS!)
        # Ao colocar as margens em zero, a barra superior cola no teto e nas laterais
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        #Barra superior
        self.barra_superior = QFrame()
        self.barra_superior.setFixedHeight(40)
        self.barra_superior.setStyleSheet("""
            QFrame {
                background-color: #236B74; /* Cor Teal (Azul Esverdeado) */
                /* Se estiver usando FramelessWindowHint, ative o radius abaixo */
                /* border-top-left-radius: 10px; border-top-right-radius: 10px; */
            }
        """)
        # Layout dentro da barra para alinhar o texto
        layout_barra = QHBoxLayout(self.barra_superior)
        layout_barra.setContentsMargins(15, 0, 15, 0)
        
        titulo = QLabel("INFORMAÇÕES DO ELETROPOSTO")
        titulo.setStyleSheet("color: white; font-weight: bold; font-family: Arial; font-size: 13px; background: transparent;")
        layout_barra.addWidget(titulo, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        
        # Adiciona a barra no topo da janela
        layout_principal.addWidget(self.barra_superior)

        # ==========================================
        # 3. ÁREA DO CONTEÚDO (Com o fundo Azul Escuro)
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
            }
        """)
        
        # Margens para não encostar na barra superior
        layout_conteudo = QVBoxLayout(self.area_conteudo)
        layout_conteudo.setContentsMargins(20, 20, 20, 20)
        layout_conteudo.setSpacing(15)

        #  FUNDO
        self.fundo_eletroposto = QLabel()


        diretorio = os.path.dirname(os.path.abspath(__file__))
        caminho_fundo = os.path.join(diretorio, "imagens", "fundo_eletroposto.png")
        
        if os.path.exists(caminho_fundo):
            pixmap_fundo = QPixmap(caminho_fundo)
            pixmap_fundo = pixmap_fundo.scaled(340, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.fundo_eletroposto.setPixmap(pixmap_fundo)
            
        layout_conteudo.addWidget(self.fundo_eletroposto, alignment=Qt.AlignHCenter)

        # Cartão exemplo
        cartao_info = QFrame()
        cartao_info.setStyleSheet("""
            QFrame {
                background-color: #1B2C42; 
                border: 1px solid #2A4365; 
                border-radius: 8px;
            }
        """)
        layout_cartao = QVBoxLayout(cartao_info)
        
        lbl_hardware = QLabel("HARDWARE")
        lbl_hardware.setStyleSheet("color: #33B5E5; font-weight: bold; border: none;") # Azul claro ciano
        lbl_modelo = QLabel("- Modelo: Eletroposto Fluvial")
        lbl_modelo.setStyleSheet("border: none;")
        
        layout_cartao.addWidget(lbl_hardware)
        layout_cartao.addWidget(lbl_modelo)
        layout_conteudo.addWidget(cartao_info)

        # Empurra tudo pra cima e o botão pro final
        layout_conteudo.addStretch()

        # --- BOTÃO FECHAR ---
        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setFixedHeight(40)
        btn_fechar.setStyleSheet("""
        QPushButton {
            background-color: rgba(10,30,80,150); color: white;
            font-size: 12px; font-weight: bold; border: 2px solid #0078d7; border-radius: 5px;          
        }
        QPushButton:hover { background-color: rgba(0,120,215,100); }
        """)
        btn_fechar.clicked.connect(self.close)
        layout_conteudo.addWidget(btn_fechar)

        # Adiciona a área de conteúdo abaixo da barra de título
        layout_principal.addWidget(self.area_conteudo)