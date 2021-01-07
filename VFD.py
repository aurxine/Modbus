from pymodbus.client.sync import ModbusSerialClient
import time
import serial

def decode(lst):
    s = '0x'
    for x in lst:
        x = hex(x)
        s += x[2:]
    return int(s,0)

def toggle_bit(number, bit_position):
    return number^(1 << bit_position-1)

class VFD_F800():
    
    def __init__(self, client, slaveAddress = 6):
        
        self.slaveAddress = slaveAddress
        self.client = client

    
    # def VFD_ON(self):
    #     GPIO.output(self.On_pin, 1)
    #     time.sleep(1)
    #     GPIO.output(self.On_pin, 0)
    
    # def VFD_OFF(self):
    #     GPIO.output(self.Off_pin, 1)
    #     time.sleep(1)
    #     GPIO.output(self.Off_pin, 0)

    def get_Address(self, address):
        self.slaveAddress = address
    
    def readOutputFrequency(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=200, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print("Frequency:", decode(res.registers))
                return decode(res.registers)*0.01
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readOutputCurrent(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=201, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print("Current:", decode(res.registers))
                return decode(res.registers)*0.1
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readOutputVoltage(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=202, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print("Voltage:", decode(res.registers))
                return decode(res.registers)*0.1
            else:
                print(res)
                return -1

        else:
            print('Cannot connect to the VFD')
            return -1
    
    def readInputPower(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=212, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print("Input Power: ", decode(res.registers))
                return decode(res.registers)*0.1*1000
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readOutputPower(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=213, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print("Output Power: ", decode(res.registers))
                return decode(res.registers)*0.1*1000
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
    
    def readCumulativePower(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=224, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print("Cumulative Power: ", decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readOutputMotor(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=233, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print("Output Motor:", decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readRunningFrequency(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=14, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1

    def readRunningSpeed(self, Print=False):
        if self.client.connect():
            print("Connected to the VFD")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=205, count=1, unit= self.slaveAddress)
            
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                return decode(res.registers)
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def readFaultHistory(self, Print = False):
        if self.client.connect():
            print("Connected to the VFD")
            response = self.client.read_holding_registers(address = 500, count = 1, unit = self.slaveAddress)
            if not response.isError():
                Fault_code = decode(response.registers)
                return Fault_code
            else:
                print(response)
                return -1
        else:
            print('Cannot connect to the VFD')
            return -1
            
    def writeRunningFrequency(self, frequency_value):
        if self.client.connect():
            print("Connected to the VFD")
            # Writing to a holding register with the below content.
            self.client.write_register(address=1000, value = frequency_value)
            
            for i in range(10):
                time.sleep(0.1)
                frequency = self.readOutputFrequency()
                if frequency == frequency_value:
                    return 1
            return -1
            
        else:
            print('Cannot connect to the VFD')
            return -1


#vfd = VFD_F800(port= 'COM13', baudrate= 9600, slaveAddress= 6)

#vfd.readOutputPower(Print= True)
