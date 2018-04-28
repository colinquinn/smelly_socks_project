class Sensor(object):
    name = ""
    avg_voltage = 0.00
           
    def __init__(self, name, SER, connection, avg_voltage, voltage):
        self.name = name
        self.SER = SER
        self.connection = connection
        self.avg_voltage = avg_voltage
        self.voltage = voltage
        
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
    
    
    
def init_sensor(name, SER):
    sensor = Sensor(name,SER)
    sensor.connection = find_ardunio(name,SER)
    time.sleep(2)
    sensor.avg_voltage = get_avg_voltage(sensor.connection)
    sensor.voltage = connection.readline().strip().replace('\r','')
    return sensor