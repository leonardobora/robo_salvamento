import os

class SimuladorLabirinto:
    def __init__(self, labirinto_ou_arquivo):
        if isinstance(labirinto_ou_arquivo, list):
            self.nome_mapa = "labirinto_teste"
            self.labirinto = labirinto_ou_arquivo
        else:
            self.nome_mapa = os.path.basename(labirinto_ou_arquivo).split('.')[0]
            self.labirinto = self.ler_mapa(labirinto_ou_arquivo)
        
        self.posicao_robo = self.encontrar_entrada()
        self.direcao_robo = self.determinar_direcao_inicial()
        self.humano_coletado = False
        self.validar_labirinto()
        print(f"Posição inicial do robô: {self.posicao_robo}")
        print(f"Direção inicial do robô: {self.direcao_robo}")

    def ler_mapa(self, arquivo_mapa):
        with open(arquivo_mapa, 'r') as arquivo:
            return [linha.strip() for linha in arquivo.readlines()]

    def encontrar_entrada(self):
        for i, linha in enumerate(self.labirinto):
            for j, celula in enumerate(linha):
                if celula == 'E':
                    return (i, j)
        raise ValueError("Entrada nao encontrada no labirinto")

    def determinar_direcao_inicial(self):
        i, j = self.posicao_robo
        if i == 0:
            return 2  # Sul
        elif i == len(self.labirinto) - 1:
            return 0  # Norte
        elif j == 0:
            return 1  # Leste
        else:
            return 3  # Oeste

    def validar_labirinto(self):
        entradas = sum(linha.count('E') for linha in self.labirinto)
        humanos = sum(linha.count('H') for linha in self.labirinto)
        
        if entradas != 1:
            raise ValueError(f"O labirinto deve ter exatamente 1 entrada. Encontradas: {entradas}")
        if humanos != 1:
            raise ValueError(f"O labirinto deve ter exatamente 1 humano. Encontrados: {humanos}")

    def obter_leituras_sensores(self):
        i, j = self.posicao_robo
        direcoes = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Norte, Leste, Sul, Oeste
        leituras = []

        for di, dj in direcoes:
            ni, nj = i + di, j + dj
            
            if 0 <= ni < len(self.labirinto) and 0 <= nj < len(self.labirinto[0]):
                celula = self.labirinto[ni][nj]
                if celula == '*':
                    leituras.append("PAREDE")
                elif celula == 'H':
                    leituras.append("HUMANO")
                else:
                    leituras.append("VAZIO")
            else:
                leituras.append("PAREDE")  # Fora dos limites do labirinto

        return leituras

    def mover_robo(self, comando):
        if comando == 'A':
            di, dj = [(-1, 0), (0, 1), (1, 0), (0, -1)][self.direcao_robo]
            nova_i, nova_j = self.posicao_robo[0] + di, self.posicao_robo[1] + dj
            if 0 <= nova_i < len(self.labirinto) and 0 <= nova_j < len(self.labirinto[0]) and self.labirinto[nova_i][nova_j] != '*':
                self.posicao_robo = (nova_i, nova_j)
            else:
                raise ValueError(f"Colisao com parede! Tentativa de mover de {self.posicao_robo} para ({nova_i}, {nova_j})")
        elif comando == 'G':
            self.direcao_robo = (self.direcao_robo + 1) % 4
        elif comando == 'P':
            leituras = self.obter_leituras_sensores()
            if "HUMANO" in leituras:
                direcao_humano = leituras.index("HUMANO")
                di, dj = [(-1, 0), (0, 1), (1, 0), (0, -1)][direcao_humano]
                i, j = self.posicao_robo
                if self.labirinto[i + di][j + dj] == 'H':
                    self.humano_coletado = True
                    self.labirinto[i + di] = self.labirinto[i + di][:j + dj] + ' ' + self.labirinto[i + di][j + dj + 1:]
                else:
                    raise ValueError("Erro ao coletar o humano")
            else:
                raise ValueError("Tentativa de coleta sem humano adjacente")
        elif comando == 'E':
            if not self.humano_coletado:
                raise ValueError("Tentativa de ejecao sem humano coletado!")
            if not self.esta_na_saida():
                raise ValueError("Tentativa de ejecao fora da saida!")
            self.humano_coletado = False

    def esta_na_saida(self):
        i, j = self.posicao_robo
        return (i == 0 or i == len(self.labirinto) - 1 or 
                j == 0 or j == len(self.labirinto[0]) - 1)
        
    def visualizar_labirinto(self):
        simbolos = {
            '*': '█',  # parede
            ' ': ' ',  # espaço vazio
            'E': 'E',  # entrada
            'H': 'H',  # humano
            'R': '►'   # robô
        }
        direcoes = ['▲', '►', '▼', '◄']

        print("\nEstado atual do labirinto:")
        for i, linha in enumerate(self.labirinto):
            linha_visual = ""
            for j, celula in enumerate(linha):
                if (i, j) == self.posicao_robo:
                    linha_visual += direcoes[self.direcao_robo]
                else:
                    linha_visual += simbolos.get(celula, celula)
            print(linha_visual)
        
        print(f"\nPosição do robô: {self.posicao_robo}")
        print(f"Direção do robô: {self.direcao_robo} ({direcoes[self.direcao_robo]})")
        print(f"Humano coletado: {'Sim' if self.humano_coletado else 'Não'}")