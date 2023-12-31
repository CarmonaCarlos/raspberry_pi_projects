import paho.mqtt.client as mqtt
from configurations import parse_app_config
import logging

# MQTT Handler
class MQTTADAFRUITHANDLER:

    def __init__(self, configPath):
        try:
            logging.info("Iniciando clase MQTTHANDLER...")
            self.config = parse_app_config(configPath, "adafruit")
            self.client = mqtt.Client(self.config.AdaFruitConfig.clientId)
            self.client.username_pw_set(self.config.AdaFruitConfig.adafruitId, self.config.AdaFruitConfig.adafruitKey)
            self.client.connect(self.config.AdaFruitConfig.brokerAddress)
            logging.info("¡MQTTHANDLER inicio correctamente!")
        except Exception as e:
            logging.error(f"Se produjo un error al inicializar el controlador MQTT.: {e}")

    def send_message(self, message):
        try:
            logging.info("Enviando mensaje al broker...")
            self.client.publish(self.config.AdaFruitConfig.pubTopic, message)
            logging.info("¡Mensaje enviado!")
        except Exception as e:
            logging.info(f"Se produjo un error al tratar de enviar el mensaje {e}")
