import json

class LocalConfig:
    def __init__(self, clientId, brokerAddress, brokerPort, pubTopic):
        self.clientId = clientId
        self.brokerAddress = brokerAddress
        self.brokerPort = brokerPort
        self.pubTopic = pubTopic

class AdaFruitConfig:
    def __init__(self, clientId, adafruitId, adafruitKey, brokerAddress, pubTopic):
        self.clientId = clientId
        self.adafruitId = adafruitId
        self.adafruitKey = adafruitKey
        self.brokerAddress = brokerAddress
        self.pubTopic = pubTopic

class AppConfiguration:
    def __init__(self, adaFruitConfig=None, localConfig=None):
        self.AdaFruitConfig = adaFruitConfig
        self.LocalConfig = localConfig

class AppConfigurationEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

        
def parse_app_config(file_path, config_type):
    try:
        with open(file_path, "r") as file:
            appJson = file.read()

        appDict = json.loads(appJson)

        if "adaFruitConfig" in appDict and config_type == "adafruit":
            adaFruitConfig = AdaFruitConfig(**appDict["adaFruitConfig"])            
            appConfig = AppConfiguration(adaFruitConfig=adaFruitConfig)
            return appConfig
        elif "localMQTT" in appDict and config_type == "local":
            localConfig = LocalConfig(**appDict["localMQTT"])
            appConfig = AppConfiguration(localConfig=localConfig)
            return appConfig
        else:
            raise KeyError("adaFruitConfig or localMQTT not found in the JSON")

    except FileNotFoundError as e:
        print(f"File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except KeyError as e:
        print(f"Key error in JSON file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
