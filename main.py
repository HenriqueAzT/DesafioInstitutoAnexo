import cv2
import torch
import time
import os
import tkinter as tk
import csv

from collections import deque
from PIL import Image, ImageTk
from threading import Thread
from datetime import datetime
from queue import Queue
from reportlab.pdfgen import canvas

class App:
    def __init__(self, root, cap):
        self.root = root
        self.cap = cap
        self.entryXCoordinate = 500
        self.confidenceThreshold = 0.7
        self.minDistanceToCount = 30
        self.visitorPrizeLimit = 2
        self.peopleCount = 0
        self.positionsQueue = deque(maxlen=5)
        self.personCounted = False
        self.visitorData = []

        # Adiciona um Canvas para exibir a imagem
        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        # Configuração do botão para gerar relatório
        self.reportButton = tk.Button(root, text="Gerar Relatório", command=self.generateReport)
        self.reportButton.pack()

        # Configuração do botão para fechar
        self.closeButton = tk.Button(root, text="Fechar", command=self.onClosing)
        self.closeButton.pack()

        # Usa uma fila para passar os quadros entre threads
        self.frameQueue = Queue()

        # Adiciona uma variável de instância para armazenar a última imagem
        self.lastImage = None

        # Adiciona uma variável para controlar o tempo de exibição da mensagem de parabéns
        self.messageDisplayTime = 0

        # Adiciona uma variável de sinalização para indicar que a thread deve parar
        self.threadRunning = True

        # Adiciona uma variável para o tempo de exibição da mensagem de parabéns
        self.congratulationsDisplayTime = 5  #segundos

        # Inicia a thread para a detecção de pessoas
        self.detectionThread = Thread(target=self.detectPeople)
        self.detectionThread.start()

        # Inicia a atualização periódica da imagem
        self.updateImage()

    def detectPeople(self):
        while self.threadRunning:
            ret, frame = self.cap.read()

            # Redimensiona a imagem antes da detecção
            frame = cv2.resize(frame, (640, 480))

            results = model(frame)

            pred = results.pred[0]
            labels, confidences, boxes = pred[:, -1], pred[:, -2], pred[:, :-2]

            peopleIndices = (labels == 0)
            peopleBoxes = boxes[peopleIndices]
            peopleConfidences = confidences[peopleIndices]

            for box, confidence in zip(peopleBoxes, peopleConfidences):
                x, y, w, h = map(int, box)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f'Pessoa: {confidence:.2f}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if x > self.entryXCoordinate and self.positionsQueue and (x - self.positionsQueue[0] > self.minDistanceToCount) and not self.personCounted:
                    self.peopleCount += 1
                    self.positionsQueue.clear()
                    self.personCounted = True

                    entryTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    self.visitorData.append({'Pessoa': self.peopleCount, 'Horario_Entrada': entryTime})

                    if self.peopleCount == self.visitorPrizeLimit:
                        self.messageDisplayTime = time.time() + self.congratulationsDisplayTime  # Atualiza o tempo de exibição

                elif x < self.entryXCoordinate:
                    self.personCounted = False

                self.positionsQueue.append(x)

            cv2.line(frame, (self.entryXCoordinate, 0), (self.entryXCoordinate, frame.shape[0]), (255, 0, 0), 2)
            cv2.putText(frame, f'Contagem de Pessoas: {self.peopleCount}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            frame = cv2.GaussianBlur(frame, (5, 5), 0)

            # Adiciona o quadro à fila para ser processado na GUI
            self.frameQueue.put(frame)

    def updateImage(self):
        # Verifica se há quadros na fila
        if not self.frameQueue.empty():
            # Obtem o quadro da fila
            frame = self.frameQueue.get()

            if frame is not None:
                # Atualiza a variável de instância 'lastImage'
                self.lastImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if self.lastImage is not None:
                    # Atualiza a GUI na thread principal do Tkinter
                    self.root.after(0, self.updateGui)

                    # Exibe a mensagem de parabéns se o tempo ainda não expirou
                    if time.time() < self.messageDisplayTime:
                        self.root.after(0, self.showCongratulationsMessage)

        # Chama a função novamente para continuar a atualização
        self.root.after(10, self.updateImage)

    def updateGui(self):
        # Atualiza a imagem na GUI
        img = Image.fromarray(self.lastImage)
        img = ImageTk.PhotoImage(img)

        # Limpa o conteúdo atual do Canvas e atualiza a nova imagem
        self.canvas.config(width=img.width(), height=img.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

        # Armazena uma referência ao objeto PhotoImage para evitar a coleta de lixo
        self.canvas.img = img

    def showCongratulationsMessage(self):
        self.canvas.create_text(40, 60, anchor=tk.NW, text="Parabéns, você ganhou o prêmio!", fill="red", font=("Arial", 20))

    def generatePdf(self, visitorData):
        # Gera o PDF
        pdfBaseFilename = "relatorio"
        pdfFilename = self.getUniqueFilename(pdfBaseFilename, "pdf")

        c = canvas.Canvas(pdfFilename)

        c.drawString(72, 800, "Relatório de Visitantes")

        rowHeight = 20
        x = 72
        y = 780

        for entry in visitorData:
            y -= rowHeight
            c.drawString(x, y, f"Pessoa: {entry['Pessoa']}, Horário de Entrada: {entry['Horario_Entrada']}")

        # Fecha o arquivo PDF após a conclusão
        c.save()

        # Gera o CSV
        csvFilename = "relatorio.csv"

        with open(csvFilename, 'w', newline='') as csvfile:
            fieldnames = ['Pessoa', 'Horario_Entrada']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in visitorData:
                writer.writerow(entry)

        print(f"Relatório gerado em {pdfFilename} e {csvFilename}")

    def getUniqueFilename(self, baseName, extension):
        # Adiciona sufixos numéricos até encontrar um nome de arquivo único
        count = 1
        while True:
            filename = f"{baseName}_{count}.{extension}"
            if not os.path.exists(filename):
                return filename
            count += 1

    def generateReport(self):
        self.generatePdf(self.visitorData)

    def onClosing(self):
        # Indica à thread que ela deve parar
        self.threadRunning = False
        # Espera pela thread de detecção terminar
        self.detectionThread.join()
        # Libera a câmera
        self.cap.release()
        # Destroi a janela principal
        self.root.destroy()

# Obtém o diretório do script
scriptDirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptDirectory)

model = torch.hub.load('ultralytics/yolov5:v6.0', 'yolov5s')

# Inicializa a câmera fora do bloco try-except
cap = cv2.VideoCapture(0)

# Configuração inicial da interface gráfica
root = tk.Tk()
root.title("Contador de Visitantes")

# Inicia a interface gráfica
app = App(root, cap)
root.protocol("WM_DELETE_WINDOW", app.onClosing)
root.mainloop()
