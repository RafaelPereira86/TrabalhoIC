import datetime
import paho.mqtt.client as mqtt
import json
from tkinter import *


class Modelo:
    def __init__(self):
        self.textTemp = StringVar()
        self.textLuz = StringVar()
        self.alarme = BooleanVar()
        self.textTemp.set("")
        self.textLuz.set("")
        self.alarme.set(False)

    def getTextTemp(self):
        return self.textTemp

    def setTextTemp(self, text):
        self.textTemp.set(text)

    def getTextLuz(self):
        return self.textLuz

    def setTextLuz(self, text):
        self.textLuz.set(text)

    def getAlarme(self):
        return self.alarme

    def setAlarme(self, alarme):
        self.alarme.set(alarme)


class Supervisao(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.qos = 0
        self.SERVER_TIMEOUT = 5000
        self.tempFiltrada = 24.24
        self.luzFiltrada = 0
        self.mod = Modelo()
        self.create_widgets()
        self.connect_mqtt()

    def create_widgets(self):
        self.master.title("Supervisao")
        self.grid()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # Temperatura recebida do Arduino
        labt = Label(self, text="Temperatura")
        labt.grid(row=0, column=0, padx=5, pady=5)
        self.textF = Entry(self, textvariable=self.mod.getTextTemp())
        self.textF.grid(row=0, column=1, padx=5, pady=5)

        # Luminosidade recebida do Arduino
        labl = Label(self, text="Luminosidade")
        labl.grid(row=0, column=2, padx=5, pady=5)
        self.textL = Entry(self, textvariable=self.mod.getTextLuz())
        self.textL.grid(row=0, column=3, padx=5, pady=5)

        # Botão para ativar ou desativar o alarme
        laba = Label(self, text="Alarme")
        laba.grid(row=1, column=0, padx=5, pady=5)
        self.alButton = Button(self, text="Ativar", command=self.toggle_alarme)
        self.alButton.config(bg="lightgreen")
        self.alButton.grid(row=1, column=1, padx=5, pady=5)

    def connect_mqtt(self):
        self.client = mqtt.Client(client_id="")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("/ic/Grupo0/Alarme")
        client.subscribe("/ic/Grupo0/Luminosidade")
        client.subscribe("/ic/Grupo0/Temperatura")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        payload = json.loads(msg.payload)
        if payload["tagName"] == "Temperatura":
            valor = payload["valor"].replace(",", ".")
            temp = float(valor)
            self.tempFiltrada = (self.tempFiltrada * 7 + temp) / 8
            self.mod.setTextTemp("{:.2f}".format(self.tempFiltrada))
        elif payload["tagName"] == "Luminosidade":
            valor = payload["valor"].replace(",", ".")
            luz = float(valor)
            self.luzFiltrada = (self.luzFiltrada * 7 + luz) / 8
            self.mod.setTextLuz("{:.2f}".format(self.luzFiltrada))

        self.update()

    def update(self):
        self.textF.update()
        self.textL.update()

    def toggle_alarme(self):
        alarme = self.mod.getAlarme().get()
        alarme = not alarme
        self.mod.setAlarme(alarme)
        self.publish("/ic/Grupo0/Alarme", {"tagName": "Alarme", "valor": alarme})
        self.alButton.config(text="Desativar" if alarme else "Ativar", bg="red" if alarme else "lightgreen")

    def publish(self, topic, payload):
        self.client.publish(topic, json.dumps(payload), qos=self.qos)


if __name__ == "__main__":
    root = Tk()
    app = Supervisao(master=root)
    app.mainloop()
