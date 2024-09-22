import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import Mock
from src.simulador_labirinto import SimuladorLabirinto
from src.robo_resgate import RoboResgate
from src.astar_labirinto import busca_astar
from src.visualizador import Visualizador
from src.logger import Logger

class TestRoboResgate(unittest.TestCase):

    def setUp(self):
        # Define um labirinto simples para testes
        self.labirinto_simples = [
            "***E***",
            "*     *",
            "* *** *",
            "*  H  *",
            "*******"
        ]
        # Inicializa o simulador com o labirinto simples
        self.simulador = SimuladorLabirinto(self.labirinto_simples)
        # Cria um mock do logger para testes
        self.logger = Mock(spec=Logger)
        # Inicializa o robô de resgate com o simulador e o logger
        self.robo = RoboResgate(self.simulador, self.logger)

    def test_busca_astar(self):
        # Testa o algoritmo A* para encontrar um caminho no labirinto
        inicio = (1, 1)
        fim = (3, 3)
        caminho = busca_astar(self.labirinto_simples, inicio, fim)
        self.assertIsNotNone(caminho)
        self.assertEqual(caminho[0], inicio)
        self.assertEqual(caminho[-1], fim)

    def test_humano_adjacente(self):
        # Verifica se o robô detecta corretamente quando o humano está adjacente
        self.simulador.posicao_robo = (2, 3)
        self.assertTrue(self.robo.humano_adjacente())
        self.simulador.posicao_robo = (1, 1)
        self.assertFalse(self.robo.humano_adjacente())

    def test_coletar_humano(self):
        # Testa a coleta do humano pelo robô
        self.simulador.posicao_robo = (2, 3)
        self.simulador.direcao_robo = 2  # Sul
        self.robo.coletar_humano()
        self.assertTrue(self.simulador.humano_coletado)
        self.assertEqual(self.simulador.labirinto[3][3], ' ')

    def test_movimento_robo(self):
        # Testa o movimento do robô e a mudança de direção
        posicao_inicial = (1, 1)
        self.simulador.posicao_robo = posicao_inicial
        self.simulador.direcao_robo = 1  # Leste
        self.robo.executar_comando('A')
        self.assertEqual(self.simulador.posicao_robo, (1, 2))
        self.robo.executar_comando('G')
        self.assertEqual(self.simulador.direcao_robo, 2)  # Sul

    def test_ejetar_humano(self):
        # Verifica se o robô ejeta o humano corretamente na saída
        self.simulador.posicao_robo = (0, 3)  # Posição da saída
        self.simulador.humano_coletado = True
        self.robo.executar_comando('E')
        self.assertFalse(self.simulador.humano_coletado)

    def test_movimento_invalido(self):
        # Testa se o robô levanta uma exceção ao tentar mover para uma parede
        self.simulador.posicao_robo = (1, 1)
        self.simulador.direcao_robo = 3  # Oeste
        with self.assertRaises(ValueError):
            self.robo.executar_comando('A')  # Tentativa de mover para uma parede

    def test_ejetar_humano_fora_da_saida(self):
        # Verifica se o robô levanta uma exceção ao tentar ejetar o humano fora da saída
        self.simulador.posicao_robo = (1, 1)  # Não é a saída
        self.simulador.humano_coletado = True
        with self.assertRaises(ValueError):
            self.robo.executar_comando('E')

    def test_resgate_completo(self):
        # Testa o processo completo de resgate
        print("Labirinto de teste:")
        for linha in self.labirinto_simples:
            print(linha)
        try:
            self.robo.executar_resgate()
            self.assertFalse(self.simulador.humano_coletado)
            self.assertEqual(self.simulador.posicao_robo, (0, 3))
        except ValueError as e:
            self.fail(f"O resgate falhou inesperadamente: {str(e)}")

    def test_logger(self):
        # Verifica se o logger é chamado corretamente
        self.robo.executar_comando('A')
        self.logger.registrar.assert_called()

    def test_visualizador(self):
        # Testa se o visualizador é chamado corretamente
        visualizador_mock = Mock(spec=Visualizador)
        self.robo.visualizador = visualizador_mock
        self.robo.executar_comando('A')
        visualizador_mock.criar_frame.assert_called()

    def test_labirinto_sem_solucao(self):
        # Testa o comportamento do robô em um labirinto sem solução
        labirinto_sem_solucao = [
            "***E***",
            "*  *  *",
            "* *** *",
            "*  H  *",
            "*******"
        ]
        # Cria um novo simulador com o labirinto sem solução
        simulador = SimuladorLabirinto(labirinto_sem_solucao)
        
        # Instancia um novo robô de resgate com o simulador e o logger
        robo = RoboResgate(simulador, self.logger)
        
        # Verifica se uma exceção é lançada ao tentar executar o resgate
        # Nota: Pode ser mais apropriado definir uma exceção específica para este caso
        with self.assertRaises(Exception):
            robo.executar_resgate()

if __name__ == '__main__':
    # Executa todos os testes definidos neste arquivo
    unittest.main()