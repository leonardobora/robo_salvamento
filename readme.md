# Projeto de Robô de Resgate em Labirinto para a matéria de Serviços Cognitivos - 6° período de Engenharia de Software da UniBrasil

## Integrantes do Grupo

- [Leonardo Bora da Costa - 2022100913]
- [Luan Constâncio do Prado - 2021104056]
- [Gustavo de Almeida Freitas - 2022202287]
- [Brayan Wosch - 2022100986 ]

## Visão Geral do Projeto

Este projeto acadêmico consiste na implementação de um robô de resgate autônomo capaz de navegar por um labirinto, localizar um humano e resgatá-lo. O robô utiliza o algoritmo A* para encontrar o caminho mais eficiente através do labirinto, demonstrando a aplicação prática de conceitos avançados de programação e inteligência artificial (aprendizado de máquina).

## Benefícios de Aprendizagem

1. **Algoritmos de Busca**: A implementação do A* proporciona uma compreensão profunda de algoritmos de busca heurística.
2. **Estruturas de Dados**: O projeto utiliza diversas estruturas de dados, melhorando o entendimento sobre sua aplicação prática.
3. **Programação Orientada a Objetos**: A arquitetura do projeto reforça conceitos de OOP, como encapsulamento e modularidade.
4. **Testes Unitários**: A implementação de testes unitários ensina práticas de desenvolvimento seguro e confiável.
5. **Simulação de Ambientes**: O projeto oferece experiência na criação de ambientes simulados para testes de algoritmos.

## Estrutura do Código

O projeto foi dividido em vários arquivos para manter uma estrutura limpa e modular:

- `simulador_labirinto.py`: Implementa a classe SimuladorLabirinto para representar o ambiente.
- `robo_resgate.py`: Contém a lógica principal do robô de resgate.
- `astar_labirinto.py`: Implementa o algoritmo A* para a busca de caminhos.
- `visualizador.py`: Responsável pela visualização gráfica do labirinto e do robô.
- `logger.py`: Gerencia o registro de logs das ações do robô.
- `test_robo_resgate.py`: Contém os testes unitários para validar o funcionamento do robô.

## Testes Unitários e Segurança do Código

Foram implementados testes unitários abrangentes para garantir o correto funcionamento de todas as partes do sistema. Estes testes incluem:

- Verificação do algoritmo A*
- Testes de movimentação do robô
- Validação da coleta e ejeção do humano
- Testes de casos de erro e exceções

A implementação de testes unitários não só garante a robustez do código, mas também facilita futuras manutenções e melhorias no projeto.

## Conclusão

Este projeto demonstra a aplicação prática de conceitos avançados de programação e algoritmos em um cenário realista de resgate. Através da implementação cuidadosa e da estruturação modular do código, foi possível criar um sistema robusto e eficiente, proporcionando uma valiosa experiência de aprendizado em desenvolvimento de software.
