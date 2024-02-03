Relatório da Atividade - Contador de Visitantes

Objetivo:
O objetivo desta atividade foi criar um programa em Python que utiliza visão computacional para contar o número de pessoas em um ambiente e exibir uma mensagem de parabéns quando um determinado número de visitantes for alcançado.

Funcionalidades Implementadas:

1. Detecção de Pessoas
Utilização da biblioteca YOLOv5 para realizar a detecção de pessoas em um ambiente capturado pela câmera.
Desenho de caixas delimitadoras ao redor das pessoas detectadas.
Exibição da confiança da detecção para cada pessoa.
2. Contagem de Visitantes
Contagem do número de pessoas que cruzam uma linha imaginária no ambiente.
Atualização da contagem na interface gráfica.
Verificação do limite de visitantes para exibição da mensagem de parabéns.

3. Interface Gráfica
Utilização do framework Tkinter para criar uma interface gráfica simples.
Exibição da imagem capturada pela câmera em tempo real.
Botões para gerar relatório e fechar o programa.

4. Geração de Relatório em PDF e CSV
Geração de um relatório contendo informações sobre cada visita.
Utilização da biblioteca ReportLab para criar o arquivo PDF.
Criação de um arquivo CSV com as mesmas informações.

5. Exibição de Mensagem de Parabéns
Exibição de uma mensagem de parabéns quando o número limite de visitantes for alcançado.
Configuração de um tempo de exibição para a mensagem.
Execução e Utilização
Para executar o programa, é necessário ter o Python instalado, assim como as bibliotecas especificadas no código. A execução é feita a partir do terminal ou prompt de comando, digitando:

bash
Copy code
python nome_do_arquivo.py
Substitua "nome_do_arquivo.py" pelo nome do arquivo que contém o código.

Considerações Finais
O programa atingiu os objetivos propostos, proporcionando uma solução funcional para contagem de visitantes e geração de relatórios. A estrutura do código permite fácil compreensão e manutenção. Sugere-se a inclusão de mais funcionalidades, como ajuste dinâmico de parâmetros e melhoria na interface gráfica, para futuras versões.
