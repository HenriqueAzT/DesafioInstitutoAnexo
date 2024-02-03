﻿# DesafioInstitutoAnexo


## Task List:

- [x]  **Escolha do Modelo:**
    - Utilize um modelo pré-treinado para detecção de objetos. YOLO (You Only Look Once) é uma escolha sólida, e a biblioteca Ultralytics oferece uma implementação eficiente em Python.
- [x]  **Configuração da Webcam:**
    - [x]  Utilize bibliotecas como OpenCV para acessar a webcam.
    - [x]  Defina uma região na imagem da webcam como a entrada do mercado (canto esquerdo ou direito).
    
- [x]  **Contagem de Pessoas:**
    - [x]  Faça a detecção de pessoas usando o modelo treinado. Identifique quando uma pessoa cruza a entrada definida.
    - [x]  Mantenha uma contagem do número de visitantes.
- [x]  **Mensagem de Parabéns:**
    - Configure uma condição para exibir a mensagem de PARABÉNS quando o número de visitantes atingir o limite arbitrário.
- [x]  **Armazenamento de Horário:**
    - Registre o horário em que cada pessoa entra. Use bibliotecas como **`datetime`** em Python para obter o horário atual.
- [x]  **Armazenamento em Arquivo:**
    - Armazene os dados em um formato de sua escolha. Pode ser um arquivo CSV, JSON, ou outro formato que seja fácil de manipular.
- [x]  **Interface Gráfica (GUI):**
    - [x]  Utilize bibliotecas como Tkinter para criar uma GUI simples.
    - [x]  Exiba a imagem da webcam em tempo real.
    - [x]  Adicione um botão para gerar um relatório em PDF.
- [x]  **Geração de Relatório em PDF:**
    - [x]  Use bibliotecas como ReportLab para gerar PDFs em Python.
    - [x]  Implemente uma função que colete os dados armazenados e crie um relatório formatado em PDF.
