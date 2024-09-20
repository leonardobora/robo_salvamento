from astar_labirinto import busca_astar
from visualizador import Visualizador

class RoboResgate:
    def __init__(self, simulador, logger=None):
        """
        Inicializa o robô de resgate.
        
        :param simulador: Objeto simulador do ambiente
        :param logger: Objeto para registro de logs (opcional)
        """
        self.simulador = simulador
        self.logger = logger
        self.caminho = []
        self.mapa_conhecido = set()
        self.pilha_dfs = []
        self.posicao_humano = None
        self.labirinto = self.criar_labirinto_para_astar()
        self.visualizador = Visualizador(simulador.labirinto)

    def criar_labirinto_para_astar(self):
        """
        Cria uma representação do labirinto adequada para o algoritmo A*.
        
        :return: Lista 2D representando o labirinto
        """
        linhas = len(self.simulador.labirinto)
        colunas = len(self.simulador.labirinto[0])
        labirinto = [['*' if self.simulador.labirinto[i][j] == '*' else ' ' 
                    for j in range(colunas)] for i in range(linhas)]
        print("Labirinto para A*:")
        for linha in labirinto:
            print(''.join(linha))
        return labirinto

    def executar_resgate(self):
        """
        Executa a operação de resgate completa.
        """
        try:
            print(f"Posição inicial do robô: {self.simulador.posicao_robo}")
            print(f"Direção inicial do robô: {self.simulador.direcao_robo}")
            print("Labirinto para A*:")
            for linha in self.simulador.labirinto:
                print(linha)

            # Registra o início da busca
            if self.logger:
                self.logger.registrar('INFO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                    ['Iniciando busca pelo humano'], 'SEM CARGA')
            self.simulador.visualizar_labirinto()
            self.visualizador.criar_frame(self.simulador.posicao_robo, self.simulador.direcao_robo, self.simulador.humano_coletado)
            
            # Busca o humano
            caminho = self.buscar_humano()
            if caminho is None:
                raise ValueError("Nao foi possível encontrar um caminho para o humano")
            
            # Coleta o humano
            self.coletar_humano()
            self.simulador.visualizar_labirinto()
            self.visualizador.criar_frame(self.simulador.posicao_robo, self.simulador.direcao_robo, self.simulador.humano_coletado)
            
            # Se o humano foi coletado, retorna à saída
            if self.simulador.humano_coletado:
                if self.logger:
                    self.logger.registrar('INFO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                        ['Humano coletado, retornando a saida'], 'COM HUMANO')
                
                if self.simulador.esta_na_saida():
                    print("Robô já está na saída. Ejetando humano.")
                    self.executar_comando('E')
                else:
                    caminho_saida = self.retornar_saida()
                    if caminho_saida is None:
                        raise ValueError("Não foi possível encontrar um caminho para a saída")
                    
                    self.simulador.visualizar_labirinto()
                    self.visualizador.criar_frame(self.simulador.posicao_robo, self.simulador.direcao_robo, self.simulador.humano_coletado)
            else:
                raise ValueError("Não foi possível coletar o humano")

            print("Resgate concluído com sucesso!")

        except Exception as e:
            print(f"Erro durante o resgate: {str(e)}")
            if self.logger:
                self.logger.registrar('ERRO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                    [str(e)], 'SEM CARGA' if not self.simulador.humano_coletado else 'COM HUMANO')
            raise
        finally:
            self.visualizador.salvar_gif(f'animacao_robo_{self.simulador.nome_mapa}.gif')

    def buscar_humano(self):
        """
        Busca o humano no labirinto usando o algoritmo A*.
        
        :return: Caminho até o humano ou None se não for possível encontrar
        """
        inicio = self.simulador.posicao_robo
        fim = self.encontrar_humano()
        
        if fim is None:
            if self.logger:
                self.logger.registrar('ERRO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                    ['Humano nao encontrado'], 'SEM CARGA')
            return None

        self.caminho = busca_astar(self.labirinto, inicio, fim)
        print(f"Caminho encontrado pelo A*: {self.caminho}")
        
        if self.caminho is None:
            if self.logger:
                self.logger.registrar('ERRO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                    ['Caminho para o humano nao encontrado'], 'SEM CARGA')
            return None

        # Executa o caminho até encontrar o humano
        for i in range(1, len(self.caminho)):
            if self.humano_adjacente():
                self.posicao_humano = fim
                return self.caminho[:i+1]
            self.mover_para(self.caminho[i])

        self.posicao_humano = fim
        return self.caminho

    def mover_para(self, posicao_alvo):
        """
        Move o robô para uma posição alvo.
        
        :param posicao_alvo: Tupla (x, y) representando a posição alvo
        """
        atual = self.simulador.posicao_robo
        dx = posicao_alvo[0] - atual[0]
        dy = posicao_alvo[1] - atual[1]
        
        # Determina a direção alvo
        if dx == 1:
            direcao_alvo = 2  # Sul
        elif dx == -1:
            direcao_alvo = 0  # Norte
        elif dy == 1:
            direcao_alvo = 1  # Leste
        elif dy == -1:
            direcao_alvo = 3  # Oeste
        else:
            return
        
        self.ajustar_direcao(direcao_alvo)
        self.executar_comando('A')
        
    def humano_adjacente(self):
        """
        Verifica se o humano está adjacente ao robô.
        
        :return: True se o humano estiver adjacente, False caso contrário
        """
        leituras = self.simulador.obter_leituras_sensores()
        return "HUMANO" in leituras
    
    def direcao_humano(self):
        """
        Determina a direção do humano em relação ao robô.
        
        :return: Índice da direção do humano ou None se não encontrado
        """
        leituras = self.simulador.obter_leituras_sensores()
        if "HUMANO" in leituras:
            return leituras.index("HUMANO")
        return None

    def encontrar_humano(self):
        """
        Encontra a posição do humano no labirinto.
        
        :return: Tupla (x, y) com a posição do humano ou None se não encontrado
        """
        for i, linha in enumerate(self.simulador.labirinto):
            for j, celula in enumerate(linha):
                if celula == 'H':
                    return (i, j)
        if self.logger:
            self.logger.registrar('ERRO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                  ['Humano no encontrado no labirinto'], 'SEM CARGA')
        return None 

    def executar_caminho(self, caminho):
        """
        Executa um caminho dado.
        
        :param caminho: Lista de posições (x, y) representando o caminho
        """
        if self.logger:
            self.logger.registrar('INFO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                  [f'Iniciando execucao do caminho: {caminho}'], 'SEM CARGA')
        for i in range(1, len(caminho)):
            self.mover_para(caminho[i])

    def ajustar_direcao(self, direcao_alvo):
        """
        Ajusta a direção do robô para a direção alvo.
        
        :param direcao_alvo: Direção desejada (0-3)
        """
        while self.simulador.direcao_robo != direcao_alvo:
            self.executar_comando('G')
        print(f"Direcao ajustada para {self.simulador.direcao_robo}")

    def coletar_humano(self):
        """
        Coleta o humano se estiver adjacente ao robô.
        """
        if self.humano_adjacente():
            direcao_humano = self.direcao_humano()
            if direcao_humano is not None:
                while self.simulador.direcao_robo != direcao_humano:
                    self.executar_comando('G')
                self.executar_comando('P')
                if self.logger:
                    self.logger.registrar('INFO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                          ['Humano coletado'], 'COM HUMANO')
            else:
                if self.logger:
                    self.logger.registrar('ERRO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                          ['Humano adjacente, mas nao encontrado na leitura dos sensores'], 'SEM CARGA')
        else:
            if self.logger:
                self.logger.registrar('ERRO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                      ['Tentativa de coletar humano sem estar adjacente'], 'SEM CARGA')

    def retornar_saida(self):
        """
        Retorna à saída do labirinto após coletar o humano.
        
        :return: Caminho até a saída ou None se não for possível encontrar
        """
        inicio = self.simulador.posicao_robo
        fim = self.encontrar_saida()
        
        if inicio == fim:
            # O robô já está na saída
            self.executar_comando('E')
            return [inicio]
        
        caminho = busca_astar(self.labirinto, inicio, fim)
        
        if caminho is None:
            if self.logger:
                self.logger.registrar('ERRO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                    ['Caminho para a saida nao encontrado'], 'COM HUMANO')
            return None

        self.executar_caminho(caminho)
        self.executar_comando('E')
        return caminho

    def encontrar_saida(self):
        """
        Encontra a posição da saída no labirinto.
        
        :return: Tupla (x, y) com a posição da saída ou None se não encontrada
        """
        for i in range(len(self.simulador.labirinto)):
            if self.simulador.labirinto[i][0] == 'E':
                return (i, 0)
            if self.simulador.labirinto[i][-1] == 'E':
                return (i, len(self.simulador.labirinto[0]) - 1)
        
        for j in range(len(self.simulador.labirinto[0])):
            if self.simulador.labirinto[0][j] == 'E':
                return (0, j)
            if self.simulador.labirinto[-1][j] == 'E':
                return (len(self.simulador.labirinto) - 1, j)
        
        return None

    def executar_comando(self, comando):
        """
        Executa um comando no simulador e registra o resultado.
        
        :param comando: Comando a ser executado ('A', 'G', 'P' ou 'E')
        """
        try:
            print(f"Executando comando: {comando}")
            print(f"Posicao antes: {self.simulador.posicao_robo}, Direcao antes: {self.simulador.direcao_robo}")
            self.simulador.mover_robo(comando)
            print(f"Posicao depois: {self.simulador.posicao_robo}, Direcao depois: {self.simulador.direcao_robo}")
            leituras = self.simulador.obter_leituras_sensores()
            compartimento = 'COM HUMANO' if self.simulador.humano_coletado else 'SEM CARGA'
            if self.logger:
                self.logger.registrar(comando, self.simulador.posicao_robo, self.simulador.direcao_robo, leituras, compartimento)
            self.simulador.visualizar_labirinto()
            self.visualizador.criar_frame(self.simulador.posicao_robo, self.simulador.direcao_robo, self.simulador.humano_coletado)
        except ValueError as e:
            if self.logger:
                self.logger.registrar('ERRO', self.simulador.posicao_robo, self.simulador.direcao_robo, 
                                      [f'Erro ao executar comando {comando}: {str(e)}'], 'SEM CARGA')
            raise