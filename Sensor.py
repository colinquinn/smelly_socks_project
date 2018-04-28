import serial.tools.list_ports
import time

class Sensor(object):
    name = ""
    avg_voltage = 0.00
           
    def __init__(self, name, SER, connection, avg_voltage, voltage):
        self.name = name
        self.SER = SER
        self.connection = connection
        self.avg_voltage = avg_voltage
        self.voltage = voltage
    
def find_arduino(sensor_name, serial_number):
    for pinfo in serial.tools.list_ports.comports():
        if pinfo.serial_number == serial_number:
            print("Port opend <"+ str(pinfo.device) + "> at <14400> bits per second. Sensor array <" + str(sensor_name) + "> is operational\n")
            print(sensor_name," is connected to SER: ",serial_number)
            return serial.Serial(pinfo.device, 14400)
    print('Problem with sensor: ',sensor_name,". Make sure it is plugged into USB port")
    
def get_voltage():
        try:
            return connection.readline().strip().replace('\r','')
        except Exception:
            print("start_sensor_reader() ==> Error Converting to float")
            pass

def init_sensor(name, SER):
     connection = find_arduino(name,SER)
     time.sleep(2)
     avg_voltage = get_avg_voltage(connection)
     voltage = 5.00
     sensor = Sensor(name, SER, connection, avg_voltage, voltage)
     return sensor
    
def get_avg_voltage(connection):  
    voltage = 5 # voltage is assigned the maximun amount of voltage to begin
    voltage_array = [1000]
    voltage_population_size = 1000
        
    for i in range(0, voltage_population_size):
        voltage_array.append(0)
        try:
         serialOutput = connection.readline().strip().replace('\r','')
         voltage_array[i] = float(serialOutput)
        except Exception:
            voltage_array[i] = 0.0
            pass
        
    voltage_array = sorted(voltage_array)
    return voltage_array[900]