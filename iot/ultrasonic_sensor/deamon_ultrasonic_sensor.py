import time
import logging
import traceback
import RPi.GPIO as GPIO
from hcsr04 import HCSR04
from mqtt_local_handler import MQTTLOCALHANDLER
import daemonize
import signal
import sys

PATH_LOG = "/home/carlos/Documents/raspberry_pi_projects/iot/ultrasonic_sensor/distance_deamon.log"
PATH_CONFIG = "/home/carlos/Documents/raspberry_pi_projects/iot/ultrasonic_sensor/config.json"

def cleanup_and_exit(signum, frame, mqtt_handler, hcsr04):
    # Perform cleanup operations
    logging.info("Deteniendo el demonio: distance_deamon...")
    hcsr04.cleanup()
    mqtt_handler.client.disconnect()
    GPIO.cleanup()
    logging.info("¡Demonio finalizado correctamente!")
    sys.exit(0)

def main():
    logging.basicConfig(filename=PATH_LOG, level=logging.DEBUG)
    logging.info("Iniciando demonio distance_deamon...")

    try:
        mqtt_handler = MQTTLOCALHANDLER(configPath=PATH_CONFIG)
        hcsr04 = HCSR04(trigger=16, echo=18)

        # Register the signal handler
        signal.signal(signal.SIGTERM, lambda signum, frame: cleanup_and_exit(signum, frame, mqtt_handler, hcsr04))

        while True:
            distance = hcsr04.calculate_distance()
            mqtt_handler.send_message(str(distance))
            time.sleep(2)
    except Exception as e:
        logging.error("Ocurrió un error: %s", str(e))
        logging.error(traceback.format_exc())
        cleanup_and_exit(None, None, mqtt_handler, hcsr04)

if __name__ == "__main__":
    # Create the daemon
    daemon = daemonize.Daemonize(app="distance_daemon", pid="python_distance_daemon.pid", action=main)
    daemon.start()
