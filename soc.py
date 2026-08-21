import sys 
import os
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

# Aqui que será realizado todo envio de sinais, mais tarde implementar junto com as GPIO

class monitoramento_soc(QObject):

    # Sinais criados que enviam mensagens para a interface
    carga_atualizada = pyqtSignal(int)
    status_alterado = pyqtSignal(str)
    carregamento_concluido = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Variáveis de estado, quando inicia o carregamento
        self.carregamento_atual = False
        self.porcentagem_atual = 0

        # Valores padrão - variáveis de configuração
        self.limite_soc = 80
        self.corrente_maxima = 150 

        # O Qtimer vai atualizar a interface guiado pelo tempo simulado
        self.time = QTimer()
        self.time.timeout.connect(self.progresso_carga)

    def iniciar_carregamento(self): 
        # Neste momento, nós iniciamos o carregamento
        if not self.carregamento_atual:
            self.carregamento_atual = True # Aqui saímos do estado inicial
            self.status_alterado.emit("CARREGANDO") # Avisa na tela que o carregamento iniciou
            self.time.start(1000) # Inicia a atualização (1000ms = 1 segundo para testes)

            print(f">>> [SOC] Eletroposto carregando! Corrente máx: {self.corrente_maxima} A")

    def atualizar_configuracoes(self, novas_configuracoes):
        # Atualiza as regras se o usuário mexer no conf.py
        self.limite_soc = novas_configuracoes.get("limite_soc", 80)
        self.corrente_maxima = novas_configuracoes.get("corrente_maxima", 150)

        print(f">>> [SOC] Novas regras! O sistema agora vai parar em {self.limite_soc}% e carregar com {self.corrente_maxima} A.")

    def parar_carregamento(self):
        # Este bloco lida com a interrupção manual (botão parar)
        if self.carregamento_atual:
            self.carregamento_atual = False 
            self.status_alterado.emit("INTERROMPIDO") # Envia a mensagem que foi interrompido
            self.time.stop() # Desliga a contagem
            print(f">>> [SOC] Carregamento interrompido pelo usuário!")
    
    def progresso_carga(self):
        # Neste bloco, irá basicamente atualizar as informações guiada pelo qtimer

        # Se a bateria estiver com um valor menor que o estipulado, carrega até o limite
        if self.porcentagem_atual < self.limite_soc:
            self.porcentagem_atual += 1
            
            # Envia o novo número para a main.py atualizar o mostrador redondo
            self.carga_atualizada.emit(self.porcentagem_atual)
            
        else:
            # Se atingiu o limite estabelecido, desliga tudo automaticamente
            self.carregamento_atual = False
            self.time.stop()
            self.status_alterado.emit("CARGA COMPLETA")
            self.carregamento_concluido.emit()
            print(">>> [SOC] Carregamento Finalizado automaticamente.")