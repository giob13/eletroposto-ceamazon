import sys 
import os
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

#Aqui que será realizado todo envio de sinais, mais tarde implementar junto com as GPIO

class monitoramento_soc (QObject):

    #sinais criados que enviam mensagems para a interface
    carga_carregada = pyqtSignal(int)
    status_alterado = pyqtSignal(str)
    carregamento_concluido = pyqtSignal()

    def __init__(self):
        super().__init__()

        #variáveis de estatdo, quando inicia o carregamento
        self.carregamento_atual = False
        self.porcentagem_atual = 0

        #valores padrão - variáveis de configuração
        self.limite_soc = 80
        self.corrente_limite = 150 

        #o Qtimer vai atualizar a interface em 1 em 1 min (como estamos em fase de teste vai ajudar a emular o comportamento real)
        self.time = QTimer()
        self.time.timeout.connect(self.progresso_carga)

    def iniciar_carregamento(self): 
        #neste momento, nós iniciamos o carregamento
        if not self.carregamento_atual:
            self.carregamento_atual = True #aqui saimos do estado inicial
            self.status_alterado.emit("CARREGANDO") #avisa que na tela qu eo carrregamtno iniciou
            self.time.start(1000) #inicia a atualização

            print(f" >>> [SOC] Eletropoto carregando.! Corrente máx: {self.corrente_maxima}")

    def atualizar_configuracoes(self, novas_configuracoes):
        # Atualiza as regras se o usuário mexer no conf.py
        self.limite_soc = novas_configuracoes.get("limite_soc", 80)
        self.corrente_maxima = novas_configuracoes.get("corrente_maxima", 150)

        print(f">>> [SOC] Novas regras! O sistema agora vai parar em {self.limite_soc}% e carregar com  {self.corrente_maxima} A.")

    def parar_carregamento(self):
        #neste blocos paramos o carregamento 

        #usuário
        if self.carregamento_atual:
            self.carregamento_atual = False 
            self.status_alterado.emit("INTERROMPIDO") #envia a mensgaem que foi interrompido
            self.time.stop() #desliga a contagem

        if self.porcentagem_atual == self.limite_soc:
            self.carregamento_atual =False
            self.status_alterado.emit("CARREGADO")
            self.time.stop()
            
    def atualizar_configuracoes(self, novas_configuracoes):
            # Atualiza as regras se o usuário mexer no conf.py
            self.limite_soc = novas_configuracoes.get("limite_soc", 80)
            self.corrente_maxima = novas_configuracoes.get("corrente_maxima", 150)
    
            print(f">>> [SOC] Novas regras! O sistema agora vai parar em {self.limite_soc}% e carregar com  {self.corrente_maxima} A.")
    
    def progresso_carga (self):
        #neste bloco, irá basicamente atualizar as informações guiada pelo qtimer

        #se a bateria estiver com um valor menor que o estipulado, carrega até o limite (atualiza)
        if self.porcentagem_atual < self.limite_soc:
            self.porcentagem_atual += 1
            
            # envia o novo número para a main.py atualizar o mostrador redondo
            self.carga_atualizada.emit(self.porcentagem_atual)
            
        else:
            # se atingiu o limite estabelecido no conf.py, desliga tudo
            self.parar_carregamento()
            self.status_alterado.emit("CARGA COMPLETA")
            self.carregamento_concluido.emit()
            print(">>> [SOC] Carregamento Finalizado automaticamente.")