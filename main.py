import os
import sys
from src.simulador_labirinto import SimuladorLabirinto
from src.robo_resgate import RoboResgate
from src.logger import Logger
from src.visualizador import Visualizador

def exibir_titulo():
    titulo = """
    
░▒▓█▓▒░       ░▒▓███████▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████████████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓███████▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓████████▓▒░░▒▓█▓▒▒▓█▓▒░░▒▓██████▓▒░        ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  
░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ 
░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓██▓▒░  ░▒▓████████▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  
                                                                                                                                                                                                                                                                                                                         
    """
    print(titulo)

def listar_mapas():
    pasta_mapas = 'mapas'
    mapas = [arquivo for arquivo in os.listdir(pasta_mapas) if arquivo.endswith('.txt')]
    return mapas

def exibir_menu(mapas):
    print("\nEscolha um mapa para executar o resgate:")
    for i, mapa in enumerate(mapas, 1):
        print(f"{i}. {mapa}")
    print(f"{len(mapas) + 1}. Easter Egg")
    print("0. Sair")

def executar_resgate(mapa):
    caminho_arquivo = os.path.join('mapas', mapa)
    print(f"\nExecutando resgate para o labirinto: {mapa}")
    
    try:
        simulador = SimuladorLabirinto(caminho_arquivo)
        logger = Logger(mapa[:-4])  # Nome do arquivo sem a extensão .txt
        robo = RoboResgate(simulador, logger)
        
        robo.executar_resgate()
        
        print(f"Resgate concluído para o labirinto: {mapa}")
    except Exception as e:
        print(f"Erro durante o resgate do labirinto {mapa}: {str(e)}")
    finally:
        print("-" * 50)
        input("Pressione Enter para continuar...")

def easter_egg():
    print("\nVocê descobriu o Easter Egg!")
    print("Implementação futura: algo divertido vai acontecer aqui!")
    input("Pressione Enter para continuar...")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela
        exibir_titulo()
        mapas = listar_mapas()
        exibir_menu(mapas)
        
        escolha = input("\nDigite o número da sua escolha: ")
        
        if escolha == '0':
            print("Obrigado por usar o I SAVE HUMANS. Até a próxima!")
            sys.exit(0)
        elif escolha.isdigit():
            escolha = int(escolha)
            if 1 <= escolha <= len(mapas):
                executar_resgate(mapas[escolha - 1])
            elif escolha == len(mapas) + 1:
                easter_egg()
            else:
                print("Opção inválida. Por favor, tente novamente.")
                input("Pressione Enter para continuar...")
        else:
            print("Entrada inválida. Por favor, digite um número.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()