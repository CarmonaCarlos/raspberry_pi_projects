import paho.mqtt.client as mqtt

# CONFIG
clientID = "cm-carmona-unir"
adafruitID = "void_21"
adafruitKey = "aio_tyQT10JOUVarwWyHWHxsavIMoP1Q"
broker_address = "io.adafruit.com"
pubTopic = "{}/feeds/{}".format(adafruitID, clientID)

# MQTT Handler
class MQTTHANDLER:

    def __init__(self):
        self.client = mqtt.Client(clientID)
        self.client.username_pw_set(adafruitID, adafruitKey)
        self.client.connect(broker_address)

    def send_message(self, message):        
        print("Enviando mensaje al broker...")
        self.client.publish(pubTopic, message)
        print("Mensaje enviado!")