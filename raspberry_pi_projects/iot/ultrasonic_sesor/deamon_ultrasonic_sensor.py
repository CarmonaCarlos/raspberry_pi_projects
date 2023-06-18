import time
import logging
import traceback
import RPi.GPIO as GPIO
from hcsr04 import HCSR04
from mqtt_handler import MQTTHANDLER
import daemonize
import signal
import sys

PATH_LOG = "/home/carlos/Documents/raspberry_pi_projects/iot/ultrasonic_sesor/deamon.log"
PATH_CONFIG = "/home/carlos/Documents/raspberry_pi_projects/iot/ultrasonic_sesor/config.json"

mqtt_handler = None
hcsr04 = None

def cleanup_and_exit(signum, frame):
    # Perform cleanup operations
    hcsr04.cleanup()
    mqtt_handler.client.disconnect()
    GPIO.cleanup()
    logging.info("Finalizado correctamente!")
    sys.exit(0)

def main():
    global mqtt_handler, hcsr04

    logging.basicConfig(filename=PATH_LOG, level=logging.DEBUG)
    logging.info("Iniciando demonio distance_deamon...")
    
    try:  
        mqtt_handler = MQTTHANDLER(configPath=PATH_CONFIG)    
        hcsr04 = HCSR04(trigger=16, echo=18)

        # Register the signal handler
        signal.signal(signal.SIGTERM, cleanup_and_exit)

        while True:
            distance = hcsr04.calculate_distance()
            mqtt_handler.send_message(str(distance))
            time.sleep(2)
    except Exception as e:
        logging.error("Ocurrió un error: %s", str(e))
        logging.error(traceback.format_exc())
        cleanup_and_exit(None, None)


# Create the daemon
daemon = daemonize.Daemonize(app="distance_daemon", pid="python_distance_daemon.pid", action=main)
daemon.start()
