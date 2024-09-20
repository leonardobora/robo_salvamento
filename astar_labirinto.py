import heapq

# Definição da classe Nó para representar cada célula do labirinto
class No:
    def __init__(self, posicao, pai=None):
        self.posicao = posicao
        self.pai = pai
        self.g = 0  # Custo do caminho do início até este nó
        self.h = 0  # Heurística (estimativa do custo até o objetivo)
        self.f = 0  # Função f(n) = g(n) + h(n)

    def __lt__(self, outro):
        return self.f < outro.f

# Função para calcular a distância de Manhattan entre dois pontos
def distancia_manhattan(ponto1, ponto2):
    return abs(ponto1[0] - ponto2[0]) + abs(ponto1[1] - ponto2[1])

# Função principal do algoritmo A*
def busca_astar(labirinto, inicio, fim):
    # Criação dos nós de início e fim
    no_inicial = No(inicio)
    no_final = No(fim)

    # Listas de nós abertos e fechados
    lista_aberta = []
    lista_fechada = set()

    # Adiciona o nó inicial à lista aberta
    heapq.heappush(lista_aberta, (no_inicial.f, no_inicial))

    while lista_aberta:
        # Obtém o nó com menor valor f da lista aberta
        _, no_atual = heapq.heappop(lista_aberta)

        # Verifica se chegamos ao objetivo
        if no_atual.posicao == no_final.posicao:
            caminho = []
            while no_atual:
                caminho.append(no_atual.posicao)
                no_atual = no_atual.pai
            return caminho[::-1]  # Retorna o caminho invertido

        # Adiciona o nó atual à lista fechada
        lista_fechada.add(no_atual.posicao)

        # Gera os sucessores do nó atual
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # 4 direções: direita, baixo, esquerda, cima
            nova_posicao = (no_atual.posicao[0] + dx, no_atual.posicao[1] + dy)

            # Verifica se a nova posição é válida
            if (nova_posicao[0] < 0 or nova_posicao[0] >= len(labirinto) or
                nova_posicao[1] < 0 or nova_posicao[1] >= len(labirinto[0]) or
                labirinto[nova_posicao[0]][nova_posicao[1]] == '*'):
                continue

            # Cria um novo nó
            novo_no = No(nova_posicao, no_atual)

            # Ignora se o nó já está na lista fechada
            if novo_no.posicao in lista_fechada:
                continue

            # Calcula os valores g, h e f do novo nó
            novo_no.g = no_atual.g + 1
            novo_no.h = distancia_manhattan(novo_no.posicao, no_final.posicao)
            novo_no.f = novo_no.g + novo_no.h

            # Adiciona à lista aberta se não estiver lá ou se tiver um caminho melhor
            if not any(no.posicao == novo_no.posicao for _, no in lista_aberta):
                heapq.heappush(lista_aberta, (novo_no.f, novo_no))
            else:
                # Atualiza o nó existente se o novo caminho for melhor
                for i, (f, no) in enumerate(lista_aberta):
                    if no.posicao == novo_no.posicao and novo_no.g < no.g:
                        lista_aberta[i] = (novo_no.f, novo_no)
                        heapq.heapify(lista_aberta)
                        break

    # Se não encontrar um caminho
    return None

# Função para ler o labirinto de uma string
def ler_labirinto(texto_labirinto):
    return [list(linha) for linha in texto_labirinto.strip().split('\n')]

# Função para encontrar a posição de um caractere no labirinto
def encontrar_posicao(labirinto, caractere):
    for i, linha in enumerate(labirinto):
        for j, celula in enumerate(linha):
            if celula == caractere:
                return (i, j)
    return None

