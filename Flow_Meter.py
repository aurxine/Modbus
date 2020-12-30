from pymodbus.client.sync import ModbusSerialClient

def decode(lst):
    s = '0x'
    for x in lst:
        x = hex(x)
        s += x[2:]
    return int(s,0)


class FlowMeter_MF5712():
    
    def __init__(self, client, slaveAddress = 255):
        
        self.slaveAddress = slaveAddress
        self.client = client

    def get_Address(self, address):
        self.slaveAddress = address
    
    def read_mass_flow_meter_register_(self, Print = True):
        if self.client.connect():
            print("Flow Meter Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=2, count=1, unit= self.slaveAddress)
            #res1 = self.client.read_holding_registers(address=3, count=1, unit= self.slaveAddress)
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                    # register0=decode(res0.registers)
                    # register1=decode(res1.registers)
                    flow=((res.register[1] * 65536) + res.register[2])/1000 #mass flow in slmp
                    mass_flow=flow*1.0592
                return mass_flow
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the Flow Meter')
            return -1
    def read_flow_meter_register(self, Print = True):
        if self.client.connect():
            print("Flow Meter Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=4, count=3, unit= self.slaveAddress)
            #res1 = self.client.read_holding_registers(address=3, count=1, unit= self.slaveAddress)
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                    # register0=decode(res0.registers)
                    # register1=decode(res1.registers)
                    flow1=((res.register[1] * 65536) + res.register[2])/1000
                    flow2=res.register[3]
                    mass_flow=flow1+flow2
                return mass_flow
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the Flow Meter')
            return -1
    
    def readImportActiveEnergy(self, Print = True):
        if self.client.connect():
            print("Energy Meter Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=4, count=2, unit = self.slaveAddress)
            
            if not res.isError():
                print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the Flow Meter')
            return -1
    
#     def readExportActiveEnergy(self, Print = True):
        
#         if self.client.connect():
#             print("Energy Meter Connected to the Modbus Server/Slave")
#             # Reading from a holding register with the below content.
#             res = self.client.read_holding_registers(address=4, count=2, unit = self.slaveAddress)
            
#             if not res.isError():
#                 if Print:
#                     print(decode(res.registers))
#                 return decode(res.registers)
#             else:
#                 print(res)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
    
#     def readVoltage(self, Print = True):
        
#         if self.client.connect():
#             print("Energy Meter Connected to the Modbus Server/Slave")
#             # Reading from a holding register with the below content.
#             res = self.client.read_holding_registers(address=6, count=1, unit = self.slaveAddress)
            
#             if not res.isError():
#                 if Print:
#                     print(decode(res.registers))
#                 return decode(res.registers)/10
#             else:
#                 print(res)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
    
#     def readCurrent(self, Print = True):
        
#         if self.client.connect():
#             print("Energy Meter Connected to the Modbus Server/Slave")
#             # Reading from a holding register with the below content.
#             res = self.client.read_holding_registers(address=7, count=2, unit = self.slaveAddress)
            
#             if not res.isError():
#                 if Print:
#                     print(decode(res.registers))
#                 return decode(res.registers)/1000
#             else:
#                 print(res)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
    
#     def readActivePower(self, Print = True):
        
#         if self.client.connect():
#             print("Energy Meter Connected to the Modbus Server/Slave")
#             # Reading from a holding register with the below content.
#             res = self.client.read_holding_registers(address=9, count=2, unit = self.slaveAddress)
            
#             if not res.isError():
#                 if Print:
#                     print(decode(res.registers))
#                 return decode(res.registers)/10000
#             else:
#                 print(res)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
    
#     def readPowerFactor(self, Print = True):
        
#         if self.client.connect():
#             print("Energy Meter Connected to the Modbus Server/Slave")
#             # Reading from a holding register with the below content.
#             res = self.client.read_holding_registers(address=11, count=1, unit = self.slaveAddress)
            
#             if not res.isError():
#                 if Print:
#                     print(decode(res.registers))

#                 return decode(res.registers)/1000
#             else:
#                 print(res)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
    
#     def readFrequency(self, Print = True):
        
#         if self.client.connect():
#             print("Energy Meter Connected to the Modbus Server/Slave")
#             # Reading from a holding register with the below content.
#             res = self.client.read_holding_registers(address=12, count=1, unit = self.slaveAddress)
            
#             if not res.isError():
#                 if Print:
#                     print(decode(res.registers))
#                 return decode(res.registers)/100
#             else:
#                 print(res)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
            
    
# # dsz100 = EnergyMeter_DZS100(port='COM10', baudrate=2400)

# class EnergyMeter_DZS500():
    
#     def __init__(self, client, slaveAddress = 2):
        
#         self.slaveAddress = slaveAddress
#         self.client = client
        
#     def get_Address(self, address):
#         self.slaveAddress = address
        
#     def readCurrent(self, phase = None, Print = True):
        
#         addr = None        
#         if phase == None:
#             print("Please call with phase")
#             return
        
#         if phase == 'A':
#            addr = 16
#         elif phase == 'B':
#             addr = 17
#         elif phase == 'C':
#             addr = 18
#         else:
#             print("Please enter correct phase")
#             return 
                
#         if self.client.connect():
#             print("Connected to the Energy Meter")
#             # Reading from a holding register with the below content.
#             res = self.client.read_holding_registers(address=addr, count=1, unit = self.slaveAddress)
            
#             if not res.isError():
#                 if Print:
#                     print(decode(res.registers))
#                 return decode(res.registers)/1000
#             else:
#                 print(res)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
    
#     def readVoltage(self, phase=None, line=None, Print = True):
        
#         addr = None        
#         if phase == 'A':
#             addr = 20
#         elif phase == 'B':
#             addr = 21
#         elif phase == 'C':
#             addr = 22
#         elif line == 'AB':
#             addr = 23
#         elif line == 'BC':
#             addr = 24
#         elif line == 'CA':
#             addr = 25
#         else:
#             print("Please enter valid input")
#             return
                
#         if self.client.connect():
#             print("Connected to the Energy Meter")
#             # Reading from a holding register with the below content.
#             res = self.client.read_holding_registers(address=addr, count=1, unit = self.slaveAddress)
            
#             if not res.isError():
#                 if Print:
#                     print(decode(res.registers))
#                 return decode(res.registers)/10
#             else:
#                 print(res)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
            
#     def readPower(self, category, phase=None, Print = True):
        
#         addr = None
#         if phase == None:
#             if category == 'active':
#                 addr = 26
#             elif category == 'reactive':
#                 addr = 27
#             elif category == 'apparent':
#                 addr = 28
#             elif category == 'factor':
#                 addr = 29
                
#         elif phase == 'A':
#             if category == 'active':
#                 addr = 31
#             elif category == 'reactive':
#                 addr = 34
#             elif category == 'apparent':
#                 addr = 37
#             elif category == 'factor':
#                 addr = 40
                
#         elif phase == 'B':
#             if category == 'active':
#                 addr = 32
#             elif category == 'reactive':
#                 addr = 35
#             elif category == 'apparent':
#                 addr = 38
#             elif category == 'factor':
#                 addr = 41
                
#         elif phase == 'C':
#             if category == 'active':
#                 addr = 33
#             elif category == 'reactive':
#                 addr = 36
#             elif category == 'apparent':
#                 addr = 39
#             elif category == 'factor':
#                 addr = 42
#         if addr == None:
#             print("Invalid input")
#             return -1
   
#         if self.client.connect():
#             print("Connected to the Energy Meter")
#             # Reading from a holding register with the below content.
#             res = self.client.read_holding_registers(address=addr, count=1, unit = self.slaveAddress)
            
#             if not res.isError():
#                 if Print:
#                     print(decode(res.registers))

#                 if category == 'factor':
#                     return decode(res.registers)/1000
#                 else:
#                     return decode(res.registers)/10000
#             else:
#                 print(res)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1

#     def readBaudrate(self, Print = True):
#         if self.client.connect():
#             response = self.client.read_holding_registers(address= 129, count = 1, unit = self.slaveAddress)
#             if not response.isError():
#                 if Print:
#                     print(decode(response.registers))
#                 return decode(response.registers)
#             else:
#                 print(response)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
    
#     def changeBaudrate(self, baudrate = 9600, Print = True):
#         if self.client.connect():
#             response = self.client.write_register(address= 129, value = baudrate, unit = self.slaveAddress)
#             if not response.isError():
#                 if Print:
#                     print(response)
#             else:
#                 print(response)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1


#     def writeTime(self, value, unit='seconds'):
#         addr = None
#         if unit=='seconds':
#             addr = 500
#         elif unit=='minutes':
#             addr = 501
#         elif unit=='hour':
#             addr = 502
#         elif unit=='week':
#             addr = 503
#         elif unit=='day':
#             addr = 504
#         elif unit=='month':
#             addr = 505
#         elif unit=='year':
#             addr = 506
#         else:
#             print("Incorrect input")

#         if self.client.connect():
#             print("Connected to the Energy Meter")
#             # Reading from a holding register with the below content.
#             response = self.client.write_register(address=addr, value = value)
#             print(response)
            
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
    
#     def changeAddress(self, address = 2, Print = True):
#         if self.client.connect():
#             response = self.client.write_register(address= self.slaveAddress, value = address,
#             unit = self.slaveAddress)
#             if Print:
#                 print(response)
#                 return -1
#         else:
#             print('Cannot connect to the Energy Meter')
#             return -1
            
    
