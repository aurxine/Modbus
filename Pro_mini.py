import serial
import time

class Pro_mini():
    def __init__(self, Serial_port = '/dev/ttyUSB1', baudrate = 9600, timeout = 1, flow_unit = 'cm', time_unit = 'min',
                 flow_per_pulse = 1, past_water_flow = 10000):
        self.Serial_port = Serial_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = serial.Serial(port= self.Serial_port, baudrate= self.baudrate, timeout= self.timeout)
        self.serial.flush()
        self.commands = {"Get_Count" : 'c', "Get_Level" : 'P', "Reset_Count" : 'R', "Time" : 't',
                        "Turn_On_VFD" : 'o', "Turn_Off_VFD" : 'O', "Open_Valve" : 'V', "Close_Valve" : 'v'}
        self.flow_unit = flow_unit
        self.time_unit = time_unit
        # Water passed for each pulse in the sensor
        self.flow_per_pulse = flow_per_pulse
        # Water already passed
        self.past_water_flow = past_water_flow
        # This is for keeping track of water flow per unit time
        self.tic = time.time()
        self.toc = 0
        self.current_flow_rate = 0
        self.current_count = 0
        self.past_count = 0
        
        # This will be used for unit conversion
        # Standard unit for time is 1 second and standard unit for volume is 1 cubic meter (cm)
        # All parameters are converted to the standard unit
        self.units = {'min' : 60, 'second' : 1, 'hour' : 3600, 'day' : 24*3600, 'L' : 1000, 'cm' : 1}
    
    def give_Command(self, command):
        try:
            self.serial.write(str(command).encode('utf-8'))
        except serial.serialutil.SerialException:
            self.serial = serial.Serial(port= self.Serial_port, baudrate= self.baudrate, timeout= self.timeout)
            self.give_Command(command)

    
    def read_Response(self):
        try:
            response = self.serial.readline().decode('utf-8').rstrip()
            if len(response) != 0:
                return float(response)
            else:
                return self.read_Response()
        except serial.serialutil.SerialException:
            self.serial = serial.Serial(port= self.Serial_port, baudrate= self.baudrate, timeout= self.timeout)
            self.read_Response()


    def get_Flow_Count(self):
        self.give_Command(self.commands["Get_Count"])
        # self.serial.write(self.commands["Get_Count"])#str(led_number).encode('utf-8'))
        self.current_count = self.read_Response()#int(self.serial.readline().decode('utf-8').rstrip())
        return self.current_count

    def get_Last_Time_Interval_For_One_Pulse(self):
        self.give_Command(self.commands['Time'])
        Time = self.read_Response()
        return Time
    
    def get_Flow_Rate(self):
        water_flow_volume = self.flow_per_pulse * self.units[self.flow_unit]
        time = self.get_Last_Time_Interval_For_One_Pulse() / self.units[self.time_unit]
        if time > 0:
            return water_flow_volume / time
        return 0
    
    def put_Past_Water_Flow(self, water_flow):
        self.past_water_flow = water_flow
    
    def get_Total_Water_Passed(self):
        current_count = self.get_Flow_Count()
        self.past_water_flow += (current_count - self.past_count) * self.flow_per_pulse * self.units[self.flow_unit]
        self.past_count = current_count
        #print((current_count - self.past_count) * self.flow_per_pulse * self.units[self.flow_unit])
        #self.Reset_Count()
        return self.past_water_flow
    
    def Reset_Count(self):
        self.give_Command(self.commands["Reset_Count"])
        self.current_count = 0
        self.past_count = 0

    def put_flow_unit(self, flow_unit = 'cm'):
        self.flow_unit = flow_unit
    
    def put_time_unit(self, time_unit = 'second'):
        self.time_unit = time_unit
    
    def put_flow_per_pulse(self, flow_per_pulse):
        self.flow_per_pulse = flow_per_pulse

    def VFD_On(self):
        self.give_Command(self.commands["Turn_On_VFD"])
        # time.sleep(1)
        # self.give_Command('o')

    def VFD_Off(self):
        self.give_Command(self.commands["Turn_Off_VFD"])
        # time.sleep(1)
        # self.give_Command('f')

    def Valve_Open(self):
        self.give_Command(self.commands["Open_Valve"])

    def Valve_Close(self):
        self.give_Command(self.commands["Close_Valve"])

    def get_Pressure_Transmitter_Analog_Value(self):
        self.give_Command(self.commands["Get_Level"])
        return self.read_Response()
    

# if __name__ == "__main__":
#     pro_mini = Pro_mini(Serial_port= 'COM3')
#     while True:
#         # print(pro_mini.get_Flow_Count())
#         print(pro_mini.get_Total_Water_Passed())
#         time.sleep(2)