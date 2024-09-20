import unittest
from unittest.mock import Mock
from simulador_labirinto import SimuladorLabirinto
from robo_resgate import RoboResgate
from astar_labirinto import busca_astar
from visualizador import Visualizador
from logger import Logger

class TestRoboResgate(unittest.TestCase):

    def setUp(self):
        self.labirinto_simples = [
            "***E***",
            "*     *",
            "* *** *",
            "*  H  *",
            "*******"
        ]
        self.simulador = SimuladorLabirinto(self.labirinto_simples)
        self.logger = Mock(spec=Logger)
        self.robo = RoboResgate(self.simulador, self.logger)

    def test_busca_astar(self):
        inicio = (1, 1)
        fim = (3, 3)
        caminho = busca_astar(self.labirinto_simples, inicio, fim)
        self.assertIsNotNone(caminho)
        self.assertEqual(caminho[0], inicio)
        self.assertEqual(caminho[-1], fim)

    def test_humano_adjacente(self):
        self.simulador.posicao_robo = (2, 3)
        self.assertTrue(self.robo.humano_adjacente())
        self.simulador.posicao_robo = (1, 1)
        self.assertFalse(self.robo.humano_adjacente())

    def test_coletar_humano(self):
        self.simulador.posicao_robo = (2, 3)
        self.simulador.direcao_robo = 2  # Sul
        self.robo.coletar_humano()
        self.assertTrue(self.simulador.humano_coletado)
        self.assertEqual(self.simulador.labirinto[3][3], ' ')

    def test_movimento_robo(self):
        posicao_inicial = (1, 1)
        self.simulador.posicao_robo = posicao_inicial
        self.simulador.direcao_robo = 1  # Leste
        self.robo.executar_comando('A')
        self.assertEqual(self.simulador.posicao_robo, (1, 2))
        self.robo.executar_comando('G')
        self.assertEqual(self.simulador.direcao_robo, 2)  # Sul

    def test_ejetar_humano(self):
        self.simulador.posicao_robo = (0, 3)  # Posição da saída
        self.simulador.humano_coletado = True
        self.robo.executar_comando('E')
        self.assertFalse(self.simulador.humano_coletado)

    def test_movimento_invalido(self):
        self.simulador.posicao_robo = (1, 1)
        self.simulador.direcao_robo = 3  # Oeste
        with self.assertRaises(ValueError):
            self.robo.executar_comando('A')  # Tentativa de mover para uma parede

    def test_ejetar_humano_fora_da_saida(self):
        self.simulador.posicao_robo = (1, 1)  # Não é a saída
        self.simulador.humano_coletado = True
        with self.assertRaises(ValueError):
            self.robo.executar_comando('E')

    def test_resgate_completo(self):
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
        self.robo.executar_comando('A')
        self.logger.registrar.assert_called()

    def test_visualizador(self):
        visualizador_mock = Mock(spec=Visualizador)
        self.robo.visualizador = visualizador_mock
        self.robo.executar_comando('A')
        visualizador_mock.criar_frame.assert_called()

    def test_labirinto_sem_solucao(self):
        labirinto_sem_solucao = [
            "***E***",
            "*  *  *",
            "* *** *",
            "*  H  *",
            "*******"
        ]
        simulador = SimuladorLabirinto(labirinto_sem_solucao)
        robo = RoboResgate(simulador, self.logger)
        with self.assertRaises(Exception):  # Você pode querer definir uma exceção específica para este caso
            robo.executar_resgate()

if __name__ == '__main__':
    unittest.main()