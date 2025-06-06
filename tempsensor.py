import Adafruit_DHT as dht
import socket
import os
import paho.mqtt.publish as publish
import config


# set DATA pin
DHT = 4
hostname = str(socket.gethostname())

device_info = {
    "raspberrypi-0w1": {
        "location": "office",
        "mqqt_temp": "homeassistant/sensor/office/temperature",
        "mqqt_humid": "homeassistant/sensor/office/humidity",
    },
    "raspberrypi-0w2": {
        "location": "bedroom",
        "mqqt_temp": "homeassistant/sensor/bedroom/temperature",
        "mqqt_humid": "homeassistant/sensor/bedroom/humidity",
    },
    "raspberrypi-0w3": {
        "location": "plant",
        "mqqt_temp": "homeassistant/sensor/plant/temperature",
        "mqqt_humid": "homeassistant/sensor/plant/humidity",
    },
    "raspberrypi-0w4": {
        "location": "dining",
        "mqqt_temp": "homeassistant/sensor/dining/temperature",
        "mqqt_humid": "homeassistant/sensor/dining/humidity",
    },
}

# mqtt info
mqqt_temp_topic = device_info[hostname]["mqqt_temp"]
mqqt_humid_topic = device_info[hostname]["mqqt_humid"]

# --------- User Settings ---------
SENSOR_LOCATION_NAME = device_info[hostname]["location"]
MINUTES_BETWEEN_READS = 5
METRIC_UNITS = True
# ---------------------------------


while True:
    try:
        humidity, temp_c = dht.read_retry(dht.DHT22, DHT)

    except RuntimeError:
        print(os.path.basename.__file__)
        print("RuntimeError, trying again...")
        continue

    if METRIC_UNITS:
        temp_c = format(temp_c, ".2f")

    else:
        temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")

    humidity = format(humidity, ".2f")

    # mqtt publish
    publish.single(
        mqqt_temp_topic,
        temp_c,
        hostname=config.MQTT_SERVER,
        auth={"username": config.MQTT_user, "password": config.MQTT_password},
    )
    publish.single(
        mqqt_humid_topic,
        humidity,
        hostname=config.MQTT_SERVER,
        auth={"username": config.MQTT_user, "password": config.MQTT_password},
    )

    break
