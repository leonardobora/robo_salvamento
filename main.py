import os
from simulador_labirinto import SimuladorLabirinto
from robo_resgate import RoboResgate
from logger import Logger

def main():
    pasta_mapas = 'mapas'
    for arquivo in os.listdir(pasta_mapas):
        if arquivo.endswith('.txt'):
            caminho_arquivo = os.path.join(pasta_mapas, arquivo)
            print(f"Executando resgate para o labirinto: {arquivo}")
            
            try:
                simulador = SimuladorLabirinto(caminho_arquivo)
                logger = Logger(arquivo[:-4])  # Nome do arquivo sem a extensao .txt
                robo = RoboResgate(simulador, logger)
                
                robo.executar_resgate()
                
                print(f"Resgate concluido para o labirinto: {arquivo}")
            except Exception as e:
                print(f"Erro durante o resgate do labirinto {arquivo}: {str(e)}")
            finally:
                print("-" * 50)

if __name__ == "__main__":
    main()