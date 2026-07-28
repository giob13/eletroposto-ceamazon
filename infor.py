import os, socket, subprocess, platform
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
        self.setFixedSize(350, 400) 

        self.setAttribute(Qt.WA_StyledBackground, True)

        # Layout Principal
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

        #Conteudo
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

        #  Fundo
        self.fundo_eletroposto = QLabel(self.area_conteudo)
        self.fundo_eletroposto.setGeometry(0, 0, 370, 370)
        self.fundo_eletroposto.setAlignment(Qt.AlignCenter) 

        self.fundo_eletroposto.lower() #Envia a logo para trás

        diretorio = os.path.dirname(os.path.abspath(__file__))
        caminho_fundo = os.path.join(diretorio, "imagens", "fundo_eletroposto.png")
        
        if os.path.exists(caminho_fundo):
            pixmap_fundo = QPixmap(caminho_fundo)
            pixmap_fundo = pixmap_fundo.scaled(370, 370, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.fundo_eletroposto.setPixmap(pixmap_fundo)
            
      
        # Cartões 
        # Cartão Servidor 
        cartao_info = QFrame()
        cartao_info.setStyleSheet("""
            QFrame {
                background-color: rgba(27, 44, 66, 150); 
                border: 1px solid #2A4365; 
                border-radius: 8px;
            }
            QLabel {
                border: none; /* Remove as caixas cinzas ao redor do texto */
                background: transparent;
            }
        """)

        layout_cartaos = QVBoxLayout(cartao_info)
        layout_cartaos.setSpacing(5) # Espaço bonito entre as linhas

        # Puxando o seu dicionário de rede
        info = self.informacoes_rede()

        # título
        layout_titulo = QHBoxLayout()
        layout_titulo.setContentsMargins(0, 0, 0, 0)
        
        #para que serve?
        icone_servidor = QLabel()
        icone_servidor.setPixmap(QPixmap("caminho/para/icone.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout_titulo.addWidget(icone_servidor)

        lbl_servidor = QLabel("SERVIDOR")
        lbl_servidor.setStyleSheet("color: #33B5E5; font-weight: bold; border: none;") # Azul claro ciano
        layout_titulo.addWidget(lbl_servidor)
        layout_titulo.addStretch() # Empurra o título para a esquerda
        
        layout_cartaos.addLayout(layout_titulo)

        # Status
        layout_status = QHBoxLayout()
        layout_status.setContentsMargins(0, 0, 0, 0)

        lbl_status_rotulo = QLabel("Status:")
        lbl_status_rotulo.setStyleSheet("color: #CCCCCC; font-size: 12px;") # Cinza claro

        lbl_status_valor = QLabel(f"{info['status'].upper()}") # Converte para MAIÚSCULA
        
        # Define a cor do texto e do LED dinamicamente com base no seu dicionário
        if "conectado" in info['status'].lower():
            cor_status = "#4CAF50" # Verde
        else:
            cor_status = "#F44336" # Vermelho (se estiver offline)
            
        lbl_status_valor.setStyleSheet(f"color: {cor_status}; font-weight: bold; font-size: 12px;")

        # O LED Redondo (Luzinha)
        led_status = QLabel()
        led_status.setFixedSize(10, 10) # 10x10 pixels
        led_status.setStyleSheet(f"""
            background-color: {cor_status};
            border-radius: 5px; /* Metade do tamanho para ficar redondo perfeitamente */
        """)

        layout_status.addWidget(lbl_status_rotulo)
        layout_status.addWidget(lbl_status_valor)
        layout_status.addWidget(led_status)
        layout_status.addStretch() # Empurra tudo para a esquerda

        layout_cartaos.addLayout(layout_status)


        layout_rede = QHBoxLayout()
        layout_rede.setContentsMargins(0, 0, 0, 0)

        lbl_rede_rotulo = QLabel("IP de Rede:")
        lbl_rede_rotulo.setStyleSheet("color: #CCCCCC; font-size: 12px;")

        lbl_rede_valor = QLabel(f"{info['rede']}")
        lbl_rede_valor.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")

        layout_rede.addWidget(lbl_rede_rotulo)
        layout_rede.addWidget(lbl_rede_valor)
        layout_rede.addStretch()

        layout_cartaos.addLayout(layout_rede)

        # Finalmente, adiciona o cartão pronto na janela
        layout_conteudo.addWidget(cartao_info)


        #Cartão Hardware
        cartao_hardware = QFrame()
        cartao_hardware.setStyleSheet("""
            QFrame {
                /* Usando RGBA para dar 20 porcento de transparência e revelar a logo */
                background-color: rgba(27, 44, 66, 150); 
                border: 1px solid #2A4365; 
                border-radius: 8px;
            }
        """)

        layout_cartaoh = QVBoxLayout(cartao_hardware)

        lbl_hardware = QLabel()

        lbl_hardware = QLabel("HARDWARE")
        lbl_hardware.setStyleSheet("color: #33B5E5; font-weight: bold; border: none;")
        lbl_modelo1 = QLabel("Modelo: Eletroposto Fluvial")
        lbl_modelo1.setStyleSheet("border: none;")

        layout_cartaoh.addWidget(lbl_hardware)
        layout_cartaoh.addWidget(lbl_modelo1)
        layout_conteudo.addWidget(cartao_hardware)

        #Cartão Monitoramento 
        cartao_monitoramento = QFrame()
        cartao_monitoramento.setStyleSheet("""
            QFrame {
                /* Usando RGBA para dar 20 porcento de transparência e revelar a logo */
                background-color: rgba(27, 44, 66, 150); 
                border: 1px solid #2A4365; 
                border-radius: 8px;
            }
        """)

        layout_cartaom = QVBoxLayout(cartao_monitoramento)

        lbl_hardware = QLabel()

        lbl_monitoramento = QLabel("MONITORAMENTO")
        lbl_monitoramento.setStyleSheet("color: #33B5E5; font-weight: bold; border: none;")
        lbl_modelo2 = QLabel("Temperatura Interna: " )
        #lbl_modelo2_ = QLabel("Tensão Nominal:")
        lbl_modelo2.setStyleSheet("border: none;")

        layout_cartaom.addWidget(lbl_monitoramento)
        layout_cartaom.addWidget(lbl_modelo2)
        #layout_cartaom.addWidget(lbl_modelo2_)
        layout_conteudo.addWidget(cartao_monitoramento)

        #Cartão Manunteção 
        cartao_mauntencao = QFrame()
        cartao_mauntencao.setStyleSheet("""
            QFrame {
                /* Usando RGBA para dar 20 porcento de transparência e revelar a logo */
                background-color: rgba(27, 44, 66, 150); 
                border: 1px solid #2A4365; 
                border-radius: 8px;
            }
        """)

        layout_cartaoman = QVBoxLayout(cartao_mauntencao)

        lbl_hardware = QLabel()

        lbl_mauntencao = QLabel("MANUNTENÇÃO")
        lbl_mauntencao.setStyleSheet("color: #33B5E5; font-weight: bold; border: none;")
        #lbl_modelo3_ = QLabel("Última: ")
        lbl_modelo3 = QLabel("Próxima:")
        lbl_modelo3.setStyleSheet("border: none;")

        layout_cartaoman.addWidget(lbl_mauntencao)
        layout_cartaoman.addWidget(lbl_modelo3)
        #layout_cartaoman.addWidget(lbl_modelo3_)
        layout_conteudo.addWidget(cartao_mauntencao)


        # Empurra tudo pra cima e o botão pro final
        layout_conteudo.addStretch()

        # Botões
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
    
    def informacoes_rede(self):
        
        info = {
            "status": "Sem conexão",
            "tipo": None,
            "rede": None
        }
        
        #Verifica a conexão com a internet
        try:
            socket.create_connection(('google.com', 80), timeout=3)
            info["status"] = "Conectado"
        
        except OSError:
            return info
        
        sistema = platform.system()

        #Verifica qual sistema operacional está conectado

        #Linux
        if sistema == "Linux":
            try:
                ssid = subprocess.check_output(
                    ["iwgetid", "-r"],
                    text= True
                    ).strip()
                if ssid:
                    info["tipo"] = "Wi-fi"
                    info["rede"] = ssid

                else: 
                    info["tipo"] = "Ethernet"
                    info["rede"] = "Cabo da Rede"

            except Exception: 
                info["tipo"] = "Ethernet"
                info["rede"] = "Cabo de Rede"
        
        elif sistema == "Windows":
            try:
                resultado = subprocess.check_output(
                     ["powershell", "-Command", "Get-NetConnectionProfile | Select-Object Name,InterfaceAlias"],
                text=True
                )        

                linhas = resultado.splitlines()
                
                for linha in linhas:
                    if "Wi-Fi" in linha or "Ethernet" in linha:
                        partes = linha.split()

                        if len(partes) >= 2:
                            info["rede"] = partes[0]
                            info["tipo"] = partes[-1]
                            break

            except Exception:
                pass

        return info
    
    