import RPi.GPIO as GPIO
import time
import logging

class HCSR04:
    """Clase para calcular la distancia en sistema métrico (cm) usando GPIO con el modo BOARD"""

    SOUND_SPEED = 343  # Velocidad del sonido en metros por segundo

    def __init__(self, trigger, echo):
        try:
            logging.info("Iniciando HCSR04...")
            self.trigger = trigger
            self.echo = echo
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.trigger, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.echo, GPIO.IN)
            time.sleep(0.05)
            logging.info("¡HCSR04 iniciado correctamente!")
        except Exception as e:
            logging.error(f"Un error ha ocurrido mientras se inicializaba HCSR04: {e}")


    def calculate_distance(self):
        try:
            logging.info("Calculando distancia actual...")
            GPIO.output(self.trigger, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.trigger, GPIO.LOW)

            sonar_init = time.time()
            sonar_end = 0

            while GPIO.input(self.echo) == 0:
                sonar_init = time.time()  # Guarda el tiempo de inicio mientras el pin de eco está en estado bajo

            while GPIO.input(self.echo) == 1:
                sonar_end = time.time()  # Guarda el tiempo de fin mientras el pin de eco está en estado alto

            sonar_duration = sonar_end - sonar_init  # Calcula la duración de la señal de eco
            distance = sonar_duration * self.SOUND_SPEED * 100 / 2  # Calcula la distancia en base a la duración
            distance = round(distance, 2)  # Ajusta la distancia y la redondea a dos decimales

            logging.info("Distancia (cm): %s", str(distance))

            return distance
        except Exception as e:
            logging.error(f"Un error ha ocurrido mientras se calculaba la distancia, {e}")
            return None

    def cleanup(self):
        try:
            GPIO.cleanup()
        except Exception as e:
            logging.error(f"Un error ha ocurrido mientras se intentaba limpiar GPIO, {e}")
