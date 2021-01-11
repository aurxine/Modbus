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
pub_topic = "Test"#init.iloc[params.index('sub_topic'), 1]
sub_topic = "Test"#init.iloc[params.index('pub_topic'), 1]
broker_address = init.iloc[params.index('broker_address'), 1]
broker_port = int(init.iloc[params.index('broker_port'), 1])


def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.bad_connection_flag=True

def on_disconnect(client, userdata, rc):
    # logging.info("disconnecting reason  "  +str(rc))
    print("Client disconnected")
    client.connected_flag=False
    client.disconnect_flag=True

def on_message(client, userdata, message):
    print("Topic: " + message.topic)
    Message = str(message.payload.decode("utf-8"))
    print(Message)

MQTT_Client = mqtt.Client("Client", transport='websockets')
MQTT_Client._on_connect = on_connect
MQTT_Client.on_disconnect = on_disconnect
MQTT_Client.on_message = on_message

try:
    print("Trying to connect to broker")
    MQTT_Client.connect(broker_address, broker_port) #connect to broker
except:
    print("connection failed")
    exit(1) #Should quit or raise flag to quit or retry

try:
    print("Subscribing to topic")
    MQTT_Client.subscribe(sub_topic)
except:
    print("Subscription failed")


count = 0
MQTT_Client.loop_start()
while True:
    # MQTT_Client.loop()
    count += 1
    MQTT_Client.publish(topic=pub_topic, payload="message count: " + str(count))
    print("Inside loop")
    time.sleep(2)