'''
This code will run in Rasspberry Pi. The code will do the following,
    1. Retrieve data from VFD, Level Transmitter, Energy meter and AMR.
    2. Format the acquired data as json and send it to the broker with a unique topic
    3. Subscribe to that unique topic and receive commands
    4. Take actions according to those commands
'''
#! /usr/bin/env python

# pylint: disable=unused-variable
# pylint: enable=too-many-lines

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json
from random import seed
from random import randint
from Energy_Meter import EnergyMeter_DZS500
from Level_Transmitter import AR6451
from VFD import VFD_F800
import os
#from AMR import AMR
from pymodbus.client.sync import ModbusSerialClient
import pandas as pd
import sys
from Pro_mini import Pro_mini


class SCADA_Devices():
    def __init__(self, port = '/dev/ttyUSB0', Serial_port = '/dev/ttyUSB1', method='rtu', baudrate=9600, timeout=3, 
        parity='E', stopbits=1, bytesize=8, vfd_slaveAddress = 6, energy_meter_slaveAddress = 3, 
        level_transmitter_slaveAddress = 2, amr_flow_per_pulse = 10,
        amr_past_water_flow = 10000, ID = 1500, data_sending_period = 60, dataframe = None):
        
        #Read ID from file
        # Foysal, change this to read from the csv file
        self.dataframe = init
        self.params = list(init['parameters'])

    
        self.ID = ID        
        self.port = port
        self.method = method
        self.baudrate = baudrate
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.client = ModbusSerialClient(
            method = self.method,
            port = self.port,
            baudrate = self.baudrate,
            timeout = self.timeout,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.bytesize
        )

        self.VFD = VFD_F800(client = self.client, slaveAddress= vfd_slaveAddress)
        self.Level_Transmitter = AR6451(client = self.client, slaveAddress= level_transmitter_slaveAddress)
        self.Energy_Meter = EnergyMeter_DZS500(client = self.client, slaveAddress= energy_meter_slaveAddress)
        self.Pro_mini = Pro_mini(Serial_port = Serial_port, flow_per_pulse= amr_flow_per_pulse, 
                                    past_water_flow= amr_past_water_flow)
        self.data_sending_period = data_sending_period
        self.mqtt_client = mqtt.Client("Client", transport= 'websockets')
        self.mqtt_client.on_message = self.on_message
        self.command = ''
        self.last_command = ''
        self.mqtt_pub_topic = 'scada_test'
        self.mqtt_sub_topic = 'scada_pub'
        
        self.SCADA_Data = {
                "ID":1500,
                "Time_Stamp":"2019-11-06 16:04:52",
                "Data_Sending_Period": 60,
                "Energy":{
                    "Phase_A_Voltage":223.4,
                    "Phase_B_Voltage":223.4,
                    "Phase_C_Voltage":223.4,
                    "Line_AB_Voltage":403.2,
                    "Line_BC_Voltage":443.13,
                    "Line_CA_Voltage":392.2,
                    "Phase_A_Current":77.4,
                    "Phase_B_Current":76.5,
                    "Phase_C_Current":75.45,
                    "Active_Power":213,
                    "Power_Factor":0.56,
                    "Load":54.2
                },
                "VFD":{
                    "VFD_Status":1,
                    "Frequency":50.1,
                    "Motor_Operating_Voltage":234.1,
                    "Motor_Operating_Current":77,
                    "RPM":2414
                },
                "Water_Data":{
                    "Water_Flow":10000,
                    "Water_Pressure":341,
                    "Water_Meter_Reading":1234131,
                    "Water_Level":32
                }
            }
    
    def get_MQTT_Address(self, address = '123.49.33.109'):
        self.mqtt_address = address

    def get_MQTT_Port(self, port):
        self.mqtt_port = port

    def get_MQTT_Connection_Data(self, address, port):
        self.mqtt_address = address
        self.mqtt_port = port

        #Foysal
        #address and port will be updated here
        self.dataframe.iloc[params.index('broker_port'), 1] = port
        self.dataframe.iloc[params.index('broker_address'), 1] = address

        self.dataframe.to_csv('init.csv', index=False)

    def MQTT_Address(self):
        return self.mqtt_address
    
    def MQTT_Port(self):
        return self.mqtt_port
    
    def on_message(self, client, userdata, message):
        Message = str(message.payload.decode("utf-8"))
        self.command = Message
        print("message received:", Message)
    
    def is_New_Command(self):
        if self.last_command != self.command:
            self.last_command = self.command
            return True
        return False
    
    def get_Sub_Topic(self, topic):
        self.mqtt_sub_topic = topic
    
    def get_Pub_Topic(self, topic):
        self.mqtt_pub_topic = topic

    def connect(self):
        self.mqtt_client.connect(self.MQTT_Address(), self.MQTT_Port())

    
    def disconnect(self):
        self.mqtt_client.disconnect()
    
    def subscribe(self, topic = None):
        if topic == None:
            self.mqtt_client.subscribe(self.mqtt_sub_topic)
        else:
            self.mqtt_sub_topic = topic
            self.mqtt_client.subscribe(self.mqtt_sub_topic)
    
    def publish(self, topic = None, payload = ''):
        if topic == None:
            self.mqtt_client.publish(self.mqtt_pub_topic, payload, retain= True, qos= 1)
        else:
            self.mqtt_pub_topic = topic
            self.mqtt_client.publish(self.mqtt_pub_topic, payload, retain= True, qos= 1)
    
    def loop(self):
        self.mqtt_client.loop()


    def get_ID(self, ID):
        self.ID = ID

    def get_VFD_Address(self, address = 0):
        self.VFD.get_Address(address= address)
    
    def get_Energy_Meter_Address(self, address = 3):
        self.Energy_Meter.get_Address(address= address)
    
    def get_Level_Transmitter_Address(self, address = 2):
        self.Level_Transmitter.get_Address(address= address)
        
    def makeTimeStamp(self):
        now = datetime.now()
        self.formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return self.formatted_date_time
    
    def parameterQuery(self, type = '', parameter = ''): # returns parameters
        self.updateParameters()

        if len(type) > 0:
            return self.SCADA_Data[type][parameter]
        else:
            return self.SCADA_Data[parameter]
    
    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def executeCommand(self, json_command):
        if self.is_json(json_command):
            command = json.loads(json_command)
        else:
            self.mqtt_client.publish(self.mqtt_pub_topic, "Wrong json format")
            return 0

        if command["Command"] == "Query":
            self.mqtt_client.publish(self.mqtt_pub_topic, self.parameterQuery(type = command["Type"], parameter = command["Parameter"]))
        elif command["Command"] == "Change_ID":
            self.get_ID(command["ID"])
            self.publish(self.mqtt_pub_topic, "New ID set successfully!")
        elif command["Command"] == "Change_Data_Sending_Period":
            self.data_sending_period = int(command["Data_Sending_Period"])
            # Foysal
            # data sending period will be updated here in the fille
            self.dataframe.iloc[params.index('data_sending_period'),1] = self.data_sending_period
            self.dataframe.to_csv('init.csv', index=False)

            self.publish(self.mqtt_pub_topic, "New period " + str(self.data_sending_period) + " seconds set successfully!")
        elif command["Command"] == "Change_MQTT_Data":
            self.get_MQTT_Connection_Data(command["Address"], command["Port"])
            self.publish(self.mqtt_pub_topic, "New MQTT data set successfully!")
            self.publish(self.mqtt_pub_topic, "Restarting")
            self.restart()
        elif command["Command"] == "Change_Topic":
            #Foysal
            #add pub_topic and sub_topic to the csv file
            #new pub and sub topic will be updated here
            self.mqtt_client.unsubscribe(self.mqtt_sub_topic)
            self.mqtt_pub_topic = command["Pub_Topic"]
            self.mqtt_sub_topic = command["Sub_Topic"]
            self.mqtt_client.subscribe(self.mqtt_sub_topic)

            self.dataframe.iloc[params.index('pub_topic'), 1] = self.mqtt_pub_topic
            self.dataframe.iloc[params.index('sub_topic'), 1] = self.mqtt_sub_topic

            self.dataframe.to_csv('init.csv', index=False)
        
        elif command["Command"] == "Change_VFD_Frequency":
            frequency = int(command["Frequency"])*100
            self.VFD.writeRunningFrequency(frequency_value= frequency)
            self.publish(topic= self.mqtt_pub_topic, payload= "Frequency changed to " + str(frequency/100) + " Hz")

        elif command["Command"] == "Restart":
            self.publish(topic= self.mqtt_pub_topic, payload= "Restarting")
            self.restart()
        
        elif command["Command"] == "ON":
            self.Pro_mini.VFD_On()
            self.publish(self.mqtt_pub_topic, "VFD Turned ON")
        
        elif command["Command"] == "OFF":
            self.Pro_mini.VFD_Off()
            self.publish(self.mqtt_pub_topic, "VFD Turned OFF")

        else:
            self.publish(self.mqtt_pub_topic, "Error in command")
    
    def restart(self):
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print(output)

    def updateParameters(self, Print = False, random = False):
        self.SCADA_Data["ID"] = self.ID
        self.SCADA_Data["Time_Stamp"] = self.makeTimeStamp()
        self.SCADA_Data["Data_Sending_Period"] = self.data_sending_period

        if not random:
            self.SCADA_Data["Energy"]["Phase_A_Voltage"] = self.Energy_Meter.readVoltage(phase= 'A', Print = Print)
            self.SCADA_Data["Energy"]["Phase_B_Voltage"] = self.Energy_Meter.readVoltage(phase= 'B', Print = Print)
            self.SCADA_Data["Energy"]["Phase_C_Voltage"] = self.Energy_Meter.readVoltage(phase= 'C', Print = Print)
            self.SCADA_Data["Energy"]["Line_AB_Voltage"] = self.Energy_Meter.readVoltage(line= 'AB', Print = Print)
            self.SCADA_Data["Energy"]["Line_BC_Voltage"] = self.Energy_Meter.readVoltage(line= 'BC', Print = Print)
            self.SCADA_Data["Energy"]["Line_CA_Voltage"] = self.Energy_Meter.readVoltage(line= 'CA', Print = Print)
            self.SCADA_Data["Energy"]["Phase_A_Current"] = self.VFD.readOutputPower(Print = Print)/self.Energy_Meter.readVoltage(phase= 'A', Print = Print)
            self.SCADA_Data["Energy"]["Phase_B_Current"] = self.VFD.readOutputPower(Print = Print)/self.Energy_Meter.readVoltage(phase= 'B', Print = Print)
            self.SCADA_Data["Energy"]["Phase_C_Current"] = self.VFD.readOutputPower(Print = Print)/self.Energy_Meter.readVoltage(phase= 'C', Print = Print)
            self.SCADA_Data["Energy"]["Active_Power"] = self.VFD.readOutputPower(Print = Print)
            self.SCADA_Data["Energy"]["Power_Factor"] = self.VFD.readOutputPower(Print = Print)/self.VFD.readInputPower(Print = Print)
            self.SCADA_Data["Energy"]["Load"] = (self.SCADA_Data["Energy"]["Active_Power"]**2 - self.SCADA_Data["Energy"]["Power_Factor"]**2)**0.5
            
            if self.SCADA_Data["Energy"]["Load"] != 0:
                self.SCADA_Data["VFD"]["VFD_Status"] = 1
            else:
                self.SCADA_Data["VFD"]["VFD_Status"] = 0
            self.SCADA_Data["VFD"]["Frequency"] = self.VFD.readOutputFrequency(Print= Print)
            self.SCADA_Data["VFD"]["Motor_Operating_Voltage"] = self.VFD.readOutputVoltage(Print= Print)
            self.SCADA_Data["VFD"]["Motor_Operating_Current"] = self.VFD.readOutputCurrent(Print= Print)
            self.SCADA_Data["VFD"]["RPM"] = 3000#self.VFD.readRunningSpeed(Print= Print)

            self.SCADA_Data["Water_Data"]["Water_Flow"] = self.Pro_mini.get_Flow_Rate()
            self.SCADA_Data["Water_Data"]["Water_Pressure"] = 0 # random value
            self.SCADA_Data["Water_Data"]["Water_Meter_Reading"] = self.Pro_mini.get_Total_Water_Passed()
            self.dataframe.iloc[params.index('amr_past_water_flow'),1] = self.SCADA_Data["Water_Data"]["Water_Meter_Reading"]
            self.dataframe.to_csv('init.csv', index=False)
            self.SCADA_Data["Water_Data"]["Water_Level"] = 0#self.Level_Transmitter.Water_Level(Print= Print)
        else:
            self.SCADA_Data["Energy"]["Phase_A_Voltage"] = 240 + randint(-5, 5)/10#self.Energy_Meter.readVoltage(phase= 'A', Print = Print)
            self.SCADA_Data["Energy"]["Phase_B_Voltage"] = 240 + randint(-5, 5)/10#self.Energy_Meter.readVoltage(phase= 'B', Print = Print)
            self.SCADA_Data["Energy"]["Phase_C_Voltage"] = 240 + randint(-5, 5)/10#self.Energy_Meter.readVoltage(phase= 'C', Print = Print)
            self.SCADA_Data["Energy"]["Line_AB_Voltage"] = 415 + randint(-5, 5)/10#self.Energy_Meter.readVoltage(line= 'AB', Print = Print)
            self.SCADA_Data["Energy"]["Line_BC_Voltage"] = 415 + randint(-5, 5)/10#self.Energy_Meter.readVoltage(line= 'BC', Print = Print)
            self.SCADA_Data["Energy"]["Line_CA_Voltage"] = 415 + randint(-5, 5)/10#self.Energy_Meter.readVoltage(line= 'CA', Print = Print)
            self.SCADA_Data["Energy"]["Active_Power"] = 48900#self.VFD.readOutputPower()
            self.SCADA_Data["Energy"]["Phase_A_Current"] = self.SCADA_Data["Energy"]["Active_Power"]/self.SCADA_Data["Energy"]["Phase_A_Voltage"]
            self.SCADA_Data["Energy"]["Phase_B_Current"] = self.SCADA_Data["Energy"]["Active_Power"]/self.SCADA_Data["Energy"]["Phase_B_Voltage"]
            self.SCADA_Data["Energy"]["Phase_C_Current"] = self.SCADA_Data["Energy"]["Active_Power"]/self.SCADA_Data["Energy"]["Phase_C_Voltage"]
            
            self.SCADA_Data["Energy"]["Power_Factor"] = 0.97 + randint(-2, 2)/100
            self.SCADA_Data["Energy"]["Load"] = (self.SCADA_Data["Energy"]["Active_Power"]**2 - self.SCADA_Data["Energy"]["Power_Factor"]**2)**0.5
            
            if self.SCADA_Data["Energy"]["Load"] != 0:
                self.SCADA_Data["VFD"]["VFD_Status"] = 1
            else:
                self.SCADA_Data["VFD"]["VFD_Status"] = 0
            self.SCADA_Data["VFD"]["Frequency"] = 50
            self.SCADA_Data["VFD"]["Motor_Operating_Voltage"] = self.SCADA_Data["Energy"]["Line_AB_Voltage"]
            self.SCADA_Data["VFD"]["Motor_Operating_Current"] = self.SCADA_Data["Energy"]["Phase_A_Current"]
            self.SCADA_Data["VFD"]["RPM"] = 3000

            self.SCADA_Data["Water_Data"]["Water_Flow"] = 2 + randint(-1, 1)/10
            self.SCADA_Data["Water_Data"]["Water_Pressure"] = 341 # random value
            self.SCADA_Data["Water_Data"]["Water_Meter_Reading"] += self.SCADA_Data["Water_Data"]["Water_Flow"]
            self.SCADA_Data["Water_Data"]["Water_Level"] = 25

        return json.dumps(self.SCADA_Data)

current_folder = os.path.dirname(os.path.abspath(__file__))
init_file = os.path.join(current_folder, 'init.csv')
init = pd.read_csv(init_file)

params = list(init['parameters'])

port = init.iloc[params.index('port'), 1]
Serial_port = init.iloc[params.index('Serial_port'), 1]
method = init.iloc[params.index('method'), 1]
baudrate = int(init.iloc[params.index('baudrate'), 1])
timeout = int(init.iloc[params.index('timeout'), 1])
parity = init.iloc[params.index('parity'), 1]
stopbits = int(init.iloc[params.index('stopbits'), 1])
bytesize = int(init.iloc[params.index('bytesize'), 1])
vfd_slaveAddress = int(init.iloc[params.index('vfd_slaveAddress'), 1])
energy_meter_slaveAddress = int(init.iloc[params.index('energy_meter_slaveAddress'), 1])
level_transmitter_slaveAddress = int(init.iloc[params.index('level_transmitter_slaveAddress'), 1])
amr_flow_per_pulse = int(init.iloc[params.index('amr_flow_per_pulse'), 1])
amr_past_water_flow = int(init.iloc[params.index('amr_past_water_flow'), 1])
ID = int(init.iloc[params.index('ID'), 1])
data_sending_period = int(init.iloc[params.index('data_sending_period'), 1])

print(init)

SCADA = SCADA_Devices(port=port, Serial_port=Serial_port, method=method, baudrate=baudrate, timeout=timeout,
    parity=parity, stopbits=stopbits, bytesize=bytesize, vfd_slaveAddress=vfd_slaveAddress,
    energy_meter_slaveAddress=energy_meter_slaveAddress,
    level_transmitter_slaveAddress=level_transmitter_slaveAddress, amr_flow_per_pulse=amr_flow_per_pulse,
    amr_past_water_flow=amr_past_water_flow, ID=ID, data_sending_period=data_sending_period, dataframe=init)


broker =  init.iloc[params.index('broker_address'), 1] #'123.49.33.109' #MQTT broker address
port = int(init.iloc[params.index('broker_port'), 1]) #8083 #MQTT broker port
SCADA.get_MQTT_Address(broker)
SCADA.get_MQTT_Port(port)
SCADA.get_Sub_Topic(init.iloc[params.index('sub_topic'), 1])# Topic to publish
SCADA.get_Pub_Topic(init.iloc[params.index('pub_topic'), 1])# Topic to subscribe

SCADA.connect()
SCADA.subscribe()


tic = time.time()

while True:
    SCADA.loop()
    toc = time.time()

    if (toc - tic) >= SCADA.data_sending_period:
        SCADA_Data_Json = SCADA.updateParameters(random= False, Print = True)
        print(SCADA_Data_Json)
        SCADA.publish(payload= SCADA_Data_Json)
        tic = toc
    
    if SCADA.is_New_Command():
        print(SCADA.command)
        SCADA.executeCommand(SCADA.command)

    else:
        continue
    
    
