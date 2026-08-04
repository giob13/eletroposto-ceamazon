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

    def atualizar_configuracoes(self, novas_configuracoes):
        # Atualiza as regras se o usuário mexer no conf.py
        self.limite_soc = novas_configuracoes.get("limite_soc", 80)
        self.corrente_maxima = novas_configuracoes.get("corrente_maxima", 150)

        print(f">>> [SOC] Novas regras! O sistema agora vai parar em {self.limite_soc}% e carregar com  {self.corrente_maxima} A.")

    def progresso_carga ():