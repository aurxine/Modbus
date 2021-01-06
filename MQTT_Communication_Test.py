import paho.mqtt.client as mqtt
import os
import pandas as pd
import time


# Get current folder and read init.csv
current_folder = os.path.dirname(os.path.abspath(__file__))
init_file = os.path.join(current_folder, 'init.csv')
init = pd.read_csv(init_file)

#List out the file data
params = list(init['parameters'])

#Get Broker, Port, Subscription Topic and Publish Topic
pub_topic = init.iloc[params.index('sub_topic'), 1]
sub_topic = init.iloc[params.index('pub_topic'), 1]
broker_address = init.iloc[params.index('broker_address'), 1]
broker_port = int(init.iloc[params.index('broker_port'), 1])


def on_connect(client, userdata, flags, rc):
    print("Connected")

def on_message(client, userdata, message):
    print("Topic: " + message.topic)
    Message = str(message.payload.decode("utf-8"))
    print(Message)

MQTT_Client = mqtt.Client("Client", transport='websockets')
MQTT_Client._on_connect = on_connect
MQTT_Client.on_message = on_message

MQTT_Client.connect("123.49.33.109", port = 8083)
MQTT_Client.subscribe(sub_topic)


while True:
    MQTT_Client.publish(topic=sub_topic, payload="Hello")
    time.sleep(1)