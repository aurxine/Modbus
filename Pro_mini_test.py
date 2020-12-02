from Pro_mini import Pro_mini
import time

pro_mini = Pro_mini(Serial_port= '/dev/ttyUSB_Pro_mini')

while True:
    print("Flow Count: ", pro_mini.get_Flow_Count())
    print("Flow Rate: ", pro_mini.get_Flow_Rate())
    print("Total Water: ", pro_mini.get_Total_Water_Passed())
    time.sleep(1)