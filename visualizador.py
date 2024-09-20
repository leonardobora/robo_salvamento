import matplotlib.pyplot as plt
import numpy as np
import imageio

class Visualizador:
    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.frames = []  # Lista para armazenar os frames da animação

    def criar_frame(self, posicao_robo, direcao_robo, humano_coletado):
        # Cria uma matriz numpy do labirinto
        # 0 para espaços vazios, 1 para paredes
        matriz = np.array([[1 if c == '*' else 0 for c in linha] for linha in self.labirinto])

        # Marca a entrada/saída com o valor 2
        for i, linha in enumerate(self.labirinto):
            for j, c in enumerate(linha):
                if c == 'E':
                    matriz[i, j] = 2

        # Marca o humano com o valor 3 se ainda não foi coletado
        if not humano_coletado:
            for i, linha in enumerate(self.labirinto):
                for j, c in enumerate(linha):
                    if c == 'H':
                        matriz[i, j] = 3

        # Marca a posição do robô com o valor 4
        matriz[posicao_robo[0], posicao_robo[1]] = 4

        # Cria o plot usando matplotlib
        fig, ax = plt.subplots()
        ax.imshow(matriz, cmap='coolwarm')  # Usa um mapa de cores para visualização

        # Adiciona uma seta para indicar a direção do robô
        dy, dx = [(1, 0), (0, 1), (-1, 0), (0, -1)][direcao_robo]
        ax.arrow(posicao_robo[1], posicao_robo[0], dx*0.5, dy*0.5, 
                 head_width=0.3, head_length=0.3, fc='k', ec='k')

        # Remove os eixos para uma visualização mais limpa
        ax.axis('off')

        # Converte o plot em uma imagem e adiciona à lista de frames
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        self.frames.append(image)

        plt.close(fig)  # Fecha a figura para liberar memória

    def salvar_gif(self, nome_arquivo='animacao_robo.gif'):
        # Salva todos os frames em um arquivo GIF
        imageio.mimsave(nome_arquivo, self.frames, fps=3)
