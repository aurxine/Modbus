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
    
    def read_mass_flow_meter_register(self, Print = True):
        if self.client.connect():
            print("Flow Meter Connected to the Modbus Server/Slave")
            # Reading from a holding register with the below content.
            res = self.client.read_holding_registers(address=2, count=2, unit= self.slaveAddress)
            #res1 = self.client.read_holding_registers(address=3, count=1, unit= self.slaveAddress)
            if not res.isError():
                if Print:
                    print(decode(res.registers))
                    # register0=decode(res0.registers)
                    # register1=decode(res1.registers)
                flow=((res.registers[0] * 65536) + res.registers[1])/1000 #mass flow in slmp
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
                flow1=((res.registers[0] * 65536) + res.registers[1])/1000
                flow2=res.registers[2]
                mass_flow=flow1+flow2
                return mass_flow
            else:
                print(res)
                return -1
        else:
            print('Cannot connect to the Flow Meter')
            return -1
    

    
client = ModbusSerialClient(
            method = 'RTU',
            port = 'COM12',
            baudrate = 9600,
            timeout = 1,
            parity = 'N',
            stopbits = 1,
            bytesize = 8
        )

fm = FlowMeter_MF5712(client, 255)
mass_flow_reg = fm.read_mass_flow_meter_register(False)
flow_meter_reg = fm.read_flow_meter_register(False)
print(mass_flow_reg)
print(flow_meter_reg)