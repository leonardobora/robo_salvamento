# logger.py

import csv
from datetime import datetime

class Logger:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = f"logs/{nome_arquivo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.inicializar_arquivo()

    def inicializar_arquivo(self):
        with open(self.nome_arquivo, 'w', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['Comando', 'Posicao', 'Direcao', 'Sensor Esquerdo', 'Sensor Frente', 'Sensor Direito', 'Compartimento'])

    def registrar(self, comando, posicao, direcao, leituras, compartimento):
        with open(self.nome_arquivo, 'a', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow([comando, posicao, direcao] + leituras + [compartimento])