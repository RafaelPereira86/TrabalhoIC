import paho.mqtt.client as mqtt
import json
import random
import time

def publish_random_data():
    client = mqtt.Client(client_id="")
    client.connect("localhost", 1883, 60)

    while True:
        # Gerar valor aleatório de temperatura
        temperatura = round(random.uniform(20, 30), 2)
        payload_temp = {
            "tagName": "Temperatura",
            "valor": str(temperatura)
        }
        client.publish("/ic/Grupo0/Temperatura", json.dumps(payload_temp))
        print("Temperatura: " + str(temperatura))

        # Gerar valor aleatório de luminosidade
        luminosidade = round(random.uniform(0, 100), 2)
        payload_luz = {
            "tagName": "Luminosidade",
            "valor": str(luminosidade)
        }
        client.publish("/ic/Grupo0/Luminosidade", json.dumps(payload_luz))

        time.sleep(1)

    client.disconnect()

if __name__ == "__main__":
    publish_random_data()
