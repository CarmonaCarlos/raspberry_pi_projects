import time
import RPi.GPIO as GPIO
from hcsr04 import HCSR04
from mqtt_handler import MQTTHANDLER

def main():
    print("Iniciando...")
    try:
        mqtt_handler = MQTTHANDLER()       
        hcsr04 = HCSR04(trigger=16, echo=18)        
        while True:
            distance = hcsr04.calculate_distance()
            send_message_broker(mqtt_handler, distance)
            time.sleep(2)    
    except KeyboardInterrupt:
        print("Interrupción del teclado. Finalizando...")    
    except Exception as e:
        print("Ocurrió un error:", str(e))    
    finally:
        hcsr04.cleanup()
        mqtt_handler.client.disconnect()
        GPIO.cleanup()
        print("Finalizado correctamente!")

def send_message_broker(mqtt_handler, distance):
    message = str(distance)
    mqtt_handler.send_message(message)

if __name__ == "__main__":
    main()
