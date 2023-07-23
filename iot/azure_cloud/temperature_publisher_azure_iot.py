import time
import json
import RPi.GPIO as GPIO
from azure.iot.device import IoTHubDeviceClient
import random 

# LM35 sensor connected to GPIO 12
LM35_PIN = 12
# Debug mode
DEBUGMODE = True; 

# Function to read temperature from the LM35 sensor
def read_lm35_temperature():   
    if DEBUGMODE == True: 
        # For testing purposes, let's generate a random temperature value between 20°C and 30°C
        temperature = round(random.uniform(20, 30), 2)
        return temperature
    else : 
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LM35_PIN, GPIO.IN)

        # Read analog data from the sensor
        analog_value = 0
        for _ in range(10):
            analog_value += GPIO.input(LM35_PIN)
        analog_value /= 10

        print(analog_value)

        # Convert analog value to temperature (LM35 produces 10mV per degree Celsius change)
        voltage = (analog_value / 1023.0) * 3.3
        temperature = (voltage - 0.5) * 100

        # Cleanup GPIO
        GPIO.cleanup()
        return temperature
    

# Connection string to your IoT Hub device
CONNECTION_STRING = "HostName=iot-unir.azure-devices.net;DeviceId=raspberry-void-21-pi;SharedAccessKey=SjGbZjOl4hUbfuAO5oNW+/7qNk3J364xPVZJ+hlYlCE="

# Create an IoT Hub device client
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

# Run a loop to read temperature and send it to IoT Hub
while True:
    try:
        print(f"Getting temperature from the sensor...")
        # Read temperature from the LM35 sensor
        temperature = read_lm35_temperature()

        # Create a JSON payload
        payload = {
            "temperature": temperature
        }

        # Convert payload to JSON string
        payload_json = json.dumps(payload)
        print(f"Sending temperature to azure IoT Hub...")
        # Send the payload to IoT Hub
        device_client.send_message(payload_json)
        print(f"Temperature sent to IoT Hub: {temperature}°C")

        # Wait for some time before sending the next message
        time.sleep(5)  

    except KeyboardInterrupt:
        print("Terminating the program.")
        break

    except Exception as ex:
        print(f"Error: {ex}")
