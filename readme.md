# Projeto de Robô de Resgate em Labirinto para a matéria de Serviços Cognitivos - 6° período de Engenharia de Software da UniBrasil



                                                                                                                                                              

## Integrantes do Grupo

- [Leonardo Bora da Costa - 2022100913]
- [Luan Constâncio do Prado - 2021104056]
- [Gustavo de Almeida Freitas - 2022202287]
- [Brayan Wosch - 2022100986]

## Visão Geral do Projeto

Este projeto acadêmico consiste na implementação de um robô de resgate autônomo capaz de navegar por um labirinto, localizar um humano e resgatá-lo. O robô utiliza o algoritmo A* para encontrar o caminho mais eficiente através do labirinto, demonstrando a aplicação prática de conceitos avançados de programação e inteligência artificial.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- `src/`: Contém os arquivos fonte do projeto
  - `simulador_labirinto.py`: Implementa a classe SimuladorLabirinto para representar o ambiente
  - `robo_resgate.py`: Contém a lógica principal do robô de resgate
  - `astar_labirinto.py`: Implementa o algoritmo A* para a busca de caminhos
  - `visualizador.py`: Responsável pela visualização gráfica do labirinto e do robô
  - `logger.py`: Gerencia o registro de logs das ações do robô
- `tests/`: Contém os arquivos de teste
  - `test_robo_resgate.py`: Testes unitários para validar o funcionamento do robô
- `requirements.txt`: Lista de dependências do projeto

## Configuração do Ambiente

Para configurar o ambiente de desenvolvimento, siga estas etapas:

1. Certifique-se de ter o Python 3.8 ou superior instalado
2. Clone o repositório do projeto
3. Crie um ambiente virtual:

   ```
   python -m venv venv
   ```

4. Ative o ambiente virtual:
   - No Windows: `venv\Scripts\activate`
   - No Linux/macOS: `source venv/bin/activate`
5. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

## Executando o Projeto

Para executar o projeto, siga estas instruções:

1. Certifique-se de que o ambiente virtual está ativado
2. Execute o script principal (substitua `<script_principal.py>` pelo nome do arquivo principal):
   ```
   python src/<script_principal.py>
   ```

## Executando os Testes

Para rodar os testes unitários:

1. Certifique-se de que o ambiente virtual está ativado
2. Execute o comando:
   ```
   python -m unittest discover tests
   ```

## Benefícios de Aprendizagem

1. **Algoritmos de Busca**: Implementação do A* para compreensão de algoritmos de busca heurística
2. **Estruturas de Dados**: Utilização de diversas estruturas para aplicações práticas
3. **Programação Orientada a Objetos**: Reforço de conceitos como encapsulamento e modularidade
4. **Testes Unitários**: Práticas de desenvolvimento seguro e confiável
5. **Simulação de Ambientes**: Experiência na criação de ambientes simulados para testes de algoritmos

## Conclusão

Este projeto demonstra a aplicação prática de conceitos avançados de programação e algoritmos em um cenário realista de resgate. A implementação cuidadosa e a estruturação modular do código resultaram em um sistema robusto e eficiente, proporcionando uma valiosa experiência de aprendizado em desenvolvimento de software.
