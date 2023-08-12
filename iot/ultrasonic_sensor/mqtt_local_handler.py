import paho.mqtt.client as mqtt
from configurations import parse_app_config
import logging

# MQTT Handler
class MQTTLOCALHANDLER:

    def __init__(self, configPath):
        try:
            logging.info("Iniciando clase MQTTHANDLER...")
            self.config = parse_app_config(configPath, "local")
            self.client = mqtt.Client(self.config.LocalConfig.clientId)
            self.client.connect(self.config.LocalConfig.brokerAddress, self.config.LocalConfig.brokerPort)
            logging.info("¡MQTTHANDLER inicio correctamente!")
        except Exception as e:
            logging.error(f"Se produjo un error al inicializar el controlador MQTT.: {e}")

    def send_message(self, message):
        try:
            logging.info("Enviando mensaje al broker...")
            self.client.publish(self.config.LocalConfig.pubTopic, message)
            logging.info("¡Mensaje enviado!")
        except Exception as e:
            logging.info(f"Se produjo un error al tratar de enviar el mensaje {e}")
