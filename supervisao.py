import paho.mqtt.client as mqtt
import json

def publish_dummy_data():
    client = mqtt.Client(client_id="")
    client.connect("localhost", 1883, 60)

    # Publicar dados de temperatura
    payload_temp = {
        "tagName": "Temperatura",
        "valor": "25.00"
    }
    client.publish("/ic/Grupo0/Temperatura", json.dumps(payload_temp))

    # Publicar dados de luminosidade
    payload_luz = {
        "tagName": "Luminosidade",
        "valor": "50.00"
    }
    client.publish("/ic/Grupo0/Luminosidade", json.dumps(payload_luz))

    # Publicar estado do alarme
    payload_alarme = {
        "tagName": "Alarme",
        "valor": False
    }
    client.publish("/ic/Grupo0/Alarme", json.dumps(payload_alarme))

    client.disconnect()

if __name__ == "__main__":
    publish_dummy_data()
