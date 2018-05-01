import serial.tools.list_ports
import sys
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
        
    def take_reading(self):
        try:
            self.voltage = float(self.connection.readline().strip().replace('\r',''))
            return self.voltage
        except Exception: # Exception is caught when there is an error converting to float
            return self.avg_voltage

    
def find_arduino(sensor_name, serial_number):
    for pinfo in serial.tools.list_ports.comports():
        if pinfo.serial_number == serial_number:
            print("Sensor conected: <" + str(sensor_name) + "> is operational")
            print("Sensor Info:")
            print(" - Port opend <"+ str(pinfo.device) + "> at <14400> bits per second\n - SER: " + serial_number + "\n - USB Location: " + pinfo.location + "\n - Device: " + pinfo.manufacturer + "\n")
            return serial.Serial(pinfo.device, 14400)
    print('Problem with sensor: ',sensor_name,". Make sure it is plugged into USB port")
    

def init_sensor(name, SER):
     connection = find_arduino(name,SER)
     time.sleep(2)
     avg_voltage = get_avg_voltage(connection)
     voltage = 5.00
     sensor = Sensor(name, SER, connection, avg_voltage, voltage)
     return sensor
    
def progress(sensor_name, count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('Calibrating Sensor: <' + sensor_name + '>: [%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben
    
def get_avg_voltage(connection):  
    voltage = 5 # voltage is assigned the maximun amount of voltage to begin
    voltage_array = [1000]
    voltage_population_size = 1000
        
    for i in range(1, voltage_population_size):
        voltage_array.append(0)
        progress(connection.name, i+1,1000)
        try:
         serialOutput = connection.readline().strip().replace('\r','')
         voltage_array[i] = float(serialOutput)
        ## print(serialOutput)
        except Exception:
            voltage_array[i] = 0.0
         ##   print("Fail: 0")
            sys.exc_clear()
            pass
        
    voltage_array = sorted(voltage_array)
    print("\nAverage sensor reading: "+ str(voltage_array[100])+"\n\n")
    
    return voltage_array[100]