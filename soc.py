import sys 
import os
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

#Aqui que será realizado todo envio de sinais, mais tarde implementar junto com as GPIO

class monitoramento_soc (QObject):
    def __init__(self):
        super().__init__()

        def atualizar_configuracoes(novas_configuracoes):
        # Atualiza as regras se o usuário mexer no conf.py
            self.limite_soc = novas_configuracoes.get("limite_soc", 80)
            self.corrente_maxima = novas_configuracoes.get("corrente_maxima", 150)
            print(f">>> [SOC] Novas regras! O sistema agora vai parar em {self.limite_soc}%")