# Author: Colin O. Quinn
# Date Modified: 1/30/2018
# Email:
import os
import csv
import time
import string
import datetime
import sys
import serial
from random import randint
import chilkat
import serial.tools.list_ports
import Sensor
##import numpy

from struct import unpack
from binascii import unhexlify

#default vairables
SOCK_OWNER_NAME_1 = 'no_name_entered'
SOCK_OWNER_COUNTRY_1 = 'no_country_entered'
SOCK_OWNER_NAME_2 = 'no_name_entered'
SOCK_OWNER_COUNTRY_2 = 'no_country_entered'
CURRENT_DATE_TIME = 'system_date_error'
CSV_FILE_NAME = 'no_csv_name_assigned'
counter = 0
EXPERIMENT_PREP_TIME = 5
EXPERIMENT_RUN_TIME = 30
DATA_COLLECTED = []

welcome = '''
===================================================================================================
   _____                _ _          _____            _          _____           _           _
  / ____|              | | |        / ____|          | |        |  __ \         (_)         | |
 | (___  _ __ ___   ___| | |_   _  | (___   ___   ___| | _____  | |__) | __ ___  _  ___  ___| |_
  \___ \| '_ ` _ \ / _ \ | | | | |  \___ \ / _ \ / __| |/ / __| |  ___/ '__/ _ \| |/ _ \/ __| __|
  ____) | | | | | |  __/ | | |_| |  ____) | (_) | (__|   <\__ \ | |   | | | (_) | |  __/ (__| |_
 |_____/|_| |_| |_|\___|_|_|\__, | |_____/ \___/ \___|_|\_\___/ |_|   |_|  \___/| |\___|\___|\__|
                             __/ |                                             _/ |
                            |___/                                             |__/
===================================================================================================\n
Welcome, please wait for system tests to finish...\n
'''
sys_options = '''\
Please select one of the following:\n
1) Run Experiment
2) View CSV Library
3) Ping FTP
4) Conduct System Tests
5) Quit (or ctrl+c at anytime)
6) Run Quick Test (for demo purposes)\n

Your selection:
'''
#2) Push CSV library to server
experiment_interface = '''
Selection (1):\n
Smelly Socks Experiment Interface - Fill in Following Information
===================================================================================================
'''
experiment_Details = '''
Test Chamber Location\t\tSock Owner Name\t\t\tSock Owner Country\t\tCSV name\t\t\t
-----------------------\t\t-----------------------\t\t-----------------------\t\t-----------------------
'''
experiment_header = '''\
===================================================================================================
    !!! EXPERIMENT IN PROGRESS  !!!
===================================================================================================
'''
experiment_footer = '''\n
===================================================================================================
    !!! EXPERIMENT CONCLUDED, CLOSE GATES  !!!
===================================================================================================
    '''
experiment_summary_and_re_prompt = '''
Experiment summary:
===================================================================================================\n
- Experiment CSV has been written to ".\csv_library\ ''' + CSV_FILE_NAME + '''"
- To push the CVS(s) in csv_library, select option #2\n
===================================================================================================\n
'''
# mosquito = '''
#            _         _
#           /x\       /x\.
#          /v\x\     /v\/\.
#          \><\x\   /></x/
#           \><\x\ /></x/
#   __ __  __\><\x/></x/___
#  /##_##\/       \</x/    \__________
# |###|###|  \         \    __________\.
#  \##|##/ \__\____\____\__/          \.\.
#    |_|   |  |  | |  | |              \|
#    \*/   \  |  | |  | /              /
#            /    /
#
# '''


olfactometer = '''
#
                                    |=====================
                                    |                     |==========
                                    |                     | =========                     
        ===|========================|
                                                          |========== 
        ===|========================|                      
                                    |                     |==========
                                    |                     |
                                    |=====================|
#
# '''
def run_experiment():
    global SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, SOCK_OWNER_NAME_2, SOCK_OWNER_COUNTRY_2, CSV_FILE_NAME, CURRENT_DATE_TIME
    clear()
    print(experiment_interface)
    print('Sock Owner Name (Test Chamber 1):\n')
    SOCK_OWNER_NAME_1 = retrieve_name_from_user()
    print('\nSock Owner Country (Test Chamber 1):\n')
    SOCK_OWNER_COUNTRY_1 = retrieve_country_from_user()
    print('\nSock Owner Name (Test Chamber 2):\n')
    SOCK_OWNER_NAME_2 = retrieve_name_from_user()
    print('\nSock Owner Country (Test Chamber 2):\n')
    SOCK_OWNER_COUNTRY_2 = retrieve_country_from_user()

    CURRENT_DATE_TIME = str(datetime.datetime.now().strftime("%d-%m-%Y_%H:%M"))

    CSV_FILE_NAME = SOCK_OWNER_NAME_1.replace(' ','_').lower() + '_VS_' + SOCK_OWNER_NAME_2.replace(' ','_').lower() + '.csv'
    CSV_FILE_NAME2 = CURRENT_DATE_TIME + '.csv'
    clear()
    print('Experiment Details:')
    print(experiment_Details)
    print('Test Chamber 1'.ljust(32, ' ') + SOCK_OWNER_NAME_1.ljust(32, ' ') + SOCK_OWNER_COUNTRY_1.ljust(32, ' ') + CSV_FILE_NAME.ljust(32, ' '))# + '000000007826'.ljust(32, ' ') + '\n')
    print('Test Chamber 2'.ljust(32, ' ') + SOCK_OWNER_NAME_2.ljust(32, ' ') + SOCK_OWNER_COUNTRY_2.ljust(32, ' ') + CSV_FILE_NAME.ljust(32, ' '))# + '000000007827'.ljust(32, ' ') + '\n')
    raw_input('\nConfirm information and prep Gates. Press <enter> to begin. (You will have 5 seconds to get into place)\n ')

    print(experiment_header)
##    count_down('Open gates in', EXPERIMENT_PREP_TIME, '', False)
    start_sensor_reader()
    print(experiment_footer)

    print('CSV saved to ' + CSV_FILE_NAME + '\n\n')
    myData = []
    if yes_or_no('Rerun experiment? <y/n + enter>') == False:
        write_to_csv()
    else:
        run_experiment()

def write_to_csv():
    global SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, SOCK_OWNER_NAME_2, SOCK_OWNER_COUNTRY_2, CSV_FILE_NAME, CURRENT_DATE_TIME, counter
    DATA_COLLECTED = [[SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, CURRENT_DATE_TIME, SOCK_OWNER_NAME_2, SOCK_OWNER_COUNTRY_2, counter]] #Delete when real data is here
    csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
    new_csv_file = open('./csv_library/' + CSV_FILE_NAME, 'w')
    with new_csv_file:
        writer = csv.writer(new_csv_file, dialect = 'myDialect')
        writer.writerows(DATA_COLLECTED)
    clear()
    print(experiment_summary_and_re_prompt)
    post_csv()
    # print(sys_options)
    choose_path()

def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Please enter either y or n")
             
def pline(left,right,center):
            print("|" + left.center(30, ' ') +
              "|".ljust(30, ' ') + "|" + right.center(30, ' ') +
              "|".ljust(30, ' ') + "|" + center.center(30, ' ') + "|")



        
def start_sensor_reader():
    global counter
    counter = 0 #will count how many mosquitos have broken the plane
    voltage = 5 # voltage is assigned the maximun amount of voltage to begin
    voltage_array = [1000]
    voltage_population_size = 1000
    
##    ArduinoSerial = serial.Serial("/dev/ttyACM1", 14400)
    
## HERE!!!!! 
##    fan_arduino = find_arduino("fan_arduino",serial_number='55739323237351616062')
##    left_decision_chamber_sensor = find_arduino("left_decision_chamber",serial_number='55739323237351310101')
##    right_decision_chamber_sensor = find_arduino("right_decision_chamber",serial_number='5573932323735121C051')
##    release_chamber_sensor = find_arduino("release_chamber",serial_number='55739323237351D091A1')
    
    
##    left_decision_chamber_sensor = init_sensor("left_decision_chamber","55739323237351310101")
##    time.sleep(2) #wait for 2 secounds for the communication to get established            
##    print("Calibrating sensors...\n")
##    
##    for i in range(0, voltage_population_size):
##        voltage_array.append(0)
##        try:
##            serialOutput = left_decision_chamber_sensor.readline().strip().replace('\r','')
##            voltage_array[i] = float(serialOutput)
##        except Exception:
##            print("failed!!!!")
##            voltage_array[i] = 0.0
##            pass
##    
##    voltage_array = sorted(voltage_array)
##    left_dc_average_voltage = voltage_array[900]
##    voltage_array = []
##            
##        
##    print("Average voltage reading: " + str(left_dc_average_voltage) + "\n")
 ## TO HERE!!!!
    
    
    left_dc_sensor = Sensor.init_sensor("left_decision_chamber","55739323237351310101")
    
##    print(left_decision_chamber_sensor.name)
    
    
    count_down('Open gates in', 1, '', False) #delete after demo EXPERIMENT_PREP_TIME
    sys.stdout.write("033[K")
    t_end = time.time() + 60 * .5 #.5 is 30 seconds
    print("TEST HAS BEGUN")
    
    left_dc_voltage = 0.00
    right_dc_voltage = 0.00
    release_chamber_voltage = 0.00
    left =  ""
    center = ""
    right = ""
    
##    while time.time() < t_end:
    while 1:
        
        try:
##            left_dc_sensor.get_voltage()
####            left_dc_voltage = float(left_decision_chamber_sensor.readline().strip().replace('\r',''))
            right_dc_voltage = float(right_decision_chamber_sensor.readline().strip().replace('\r',''))
            release_chamber_voltage = float(release_chamber_sensor.readline().strip().replace('\r',''))
        except Exception:
##            print("start_sensor_reader() ==> Error Converting to float")
            pass

            
##        print("|" + get_left_dc_voltage(left_dc_average_voltage, left_dc_voltage, flag).center(10, ' ') +
##              "|".ljust(10, ' ') + "|" + str(right_dc_voltage).center(10, ' ') +
##              "|".ljust(10, ' ') + "|" + str(release_chamber_voltage).center(10, ' ') + "|")
        
##        print("|" + str(left_dc_voltage).center(10, ' ') +
##              "|".ljust(10, ' ') + "|" + str(right_dc_voltage).center(10, ' ') +
##              "|".ljust(10, ' ') + "|" + str(release_chamber_voltage).center(10, ' ') + "|")
        
        left_dc_string = ""
        
        if(left_dc_sensor.voltage < (left_dc_sensor.avg_voltage - .01)):
            counter+= 1
##            left = ("!!!!!DETECTED!!!!! Total Mosquitos: " + str(counter))
            pline("!!!!!DETECTED!!!!!",right_decision_chamber_sensor.readline().strip().replace('\r',''),release_chamber_sensor.readline().strip().replace('\r',''))
            while(((float(left_decision_chamber_sensor.readline().strip().replace('\r',''))) < (left_dc_average_voltage)) and (time.time() < t_end)):
                 pline("- not counted -",right_decision_chamber_sensor.readline().strip().replace('\r',''),release_chamber_sensor.readline().strip().replace('\r',''),)
                 try:
                    serialOutput = left_decision_chamber_sensor.readline().strip().replace('\r','')
                    left_dc_voltage = float(serialOutput)
                 except Exception:
                    print("start_sensor_reader() ==> Error Converting to float")
                    
        if(right_dc_voltage < (left_dc_sensor.avg_voltage - .01)):
            counter+= 1
##            left = ("!!!!!DETECTED!!!!! Total Mosquitos: " + str(counter))
            pline(left_dc_sensor.get_voltage(),"!!!!!DETECTED!!!!!",release_chamber_sensor.readline().strip().replace('\r',''))
            while(((float(right_decision_chamber_sensor.readline().strip().replace('\r',''))) < (left_dc_average_voltage)) and (time.time() < t_end)):
                 pline(left_dc_sensor.get_voltage(),"- not counted -",release_chamber_sensor.readline().strip().replace('\r',''),)
                 try:
                    serialOutput = right_decision_chamber_sensor.readline().strip().replace('\r','')
                    left_dc_voltage = float(serialOutput)
                 except Exception:
                    print("start_sensor_reader() ==> Error Converting to float")
        
        if(release_chamber_voltage < (left_dc_sensor.avg_voltage  - .01)):
            counter+= 1
##            left = ("!!!!!DETECTED!!!!! Total Mosquitos: " + str(counter))
            pline(left_dc_sensor.get_voltage(), right_decision_chamber_sensor.readline().strip().replace('\r',''),"!!!!!DETECTED!!!!!")
            while(((float(release_chamber_sensor.readline().strip().replace('\r',''))) < (left_dc_average_voltage)) and (time.time() < t_end)):
                 pline(left_dc_sensor.get_voltage(),right_decision_chamber_sensor.readline().strip().replace('\r',''),"- not counted -")
                 try:
                    serialOutput = release_chamber_voltage.readline().strip().replace('\r','')
                    left_dc_voltage = float(serialOutput)
                 except Exception:
                    print("start_sensor_reader() ==> Error Converting to float")
        
        
        
        
        
        
        
        
        pline(left_decision_chamber_sensor.readline().strip().replace('\r',''),release_chamber_sensor.readline().strip().replace('\r',''),right_decision_chamber_sensor.readline().strip().replace('\r',''))                   
           
           
           
           
     
           


           
##           

##                    
##        print("|   " + str(left_dc_voltage) + "   |")
##        print("|" + str(left_dc_voltage).center(10, ' ') +
##              "|".ljust(10, ' ') + "|" + str(right_dc_voltage).center(10, ' ') +
##              "|".ljust(10, ' ') + "|" + str(release_chamber_voltage).center(10, ' ') + "|")
        
        
##        if(voltage < (left_dc_average_voltage - .01)):
##            print("!!!!!DETECTED!!!!! Total Mosquitos: ")
##            counter += 1
##            print(counter)
##   
##            while(((float(left_decision_chamber_sensor.readline().strip().replace('\r',''))) < (left_dc_average_voltage)) and (time.time() < t_end)):
##                 print("-not counted-")
##                 print("|   " + str(voltage) + "   |")
##                 try:
##                    serialOutput = left_decision_chamber_sensor.readline().strip().replace('\r','')
##                    voltage = float(serialOutput)
##                 except Exception:
##                    print("start_sensor_reader() ==> Error Converting to float")
##                    sys.exit()
                    
            
            
            
            
            
            
            
            
            
    
##I started above this line!!!    
##    print("Port opend </dev/ttyACM0> at <9600> bits per second\n")
##    time.sleep(2) #wait for 2 secounds for the communication to get established
##    print("Calibrating sensors...\n")
##    
##    for i in range(0, voltage_population_size):
##        voltage_array.append(0)
##        try:
##            serialOutput = ArduinoSerial.readline().strip().replace('\r','')
##            voltage_array[i] = float(serialOutput)
##        except Exception:
##            voltage_array[i] = 0.0
##            pass
##    
##    voltage_array = sorted(voltage_array)
##    average_voltage = voltage_array[900]
    

    
    
    
##    print("Average voltage reading: ")
##    print(average_voltage)
##    print('\n')
    
##    count_down('Open gates in', 1, '', False) #delete after demo EXPERIMENT_PREP_TIME
##    sys.stdout.write("033[K")
##    t_end = time.time() + 60 * .5 #.5 is 30 seconds
##    print("TEST HAS BEGUN")
##    
####    while time.time() < t_end:
##    while 1:
####        print(ArduinoSerial.readline().strip().replace('\r',''))
##        
##        
##        try:
##            serialOutput = ArduinoSerial.readline().strip().replace('\r','')
##            voltage = float(serialOutput)
##        except Exception:
##            print("start_sensor_reader() ==> Error Converting to float")
##            sys.exc_clear() 
##        print(voltage)
##
##
##        
##        
##        if(voltage < (average_voltage - .1)):
##            print("!!!!!DETECTED!!!!! Total Mosquitos: ")
##            counter += 1
##            print(counter)
##   
##            while(((float(ArduinoSerial.readline().strip().replace('\r',''))) < (average_voltage)) and (time.time() < t_end)):
##                 print("-not counted-")
##                 print(voltage)
##                 try:
##                    serialOutput = ArduinoSerial.readline().strip().replace('\r','')
##                    voltage = float(serialOutput)
##                 except Exception:
##                    print("start_sensor_reader() ==> Error Converting to float")
##                    sys.exc_clear()
##
##            
            
            ##For M&M
            
##        if(voltage < (average_voltage - .05)):
##            print("!!!!!DETECTED!!!!! Total Mosquitos: ")
##            counter += 1
##            print(counter)
##   
##            while(((float(ArduinoSerial.readline().strip().replace('\r',''))) < (average_voltage)) and (time.time() < t_end)):
##                 print("-not counted-")
##                 print(voltage)
##                 try:
##                    serialOutput = ArduinoSerial.readline().strip().replace('\r','')
##                    voltage = float(serialOutput)
##                 except Exception:
##                    print("start_sensor_reader() ==> Error Converting to float")
##                    sys.exc_clear()

    print("!!!!!!!!!!!!!!DONE!!!!!!!!!!!!!!\n")
    print("A total of ")
    print(counter)
    print("mosqutios were detected")

def count_down(front_message, sleep_time, back_message, blank_sleep):
    if blank_sleep is False:
        for remaining in range(sleep_time, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write(front_message + "{:2d} ".format(remaining) + back_message)
            sys.stdout.flush()
            time.sleep(1)
        print('\n')
    else:
            time.sleep(sleep_time)

def print_csv_library():
    with open('./csv_library/test_csv.csv') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            print(row)

def retrieve_name_from_user():
    name = None
    while not name:
        try:
            name = str(raw_input())
        except ValueError:
            print 'Invalid Name'
    return name

def retrieve_country_from_user():
    country = None
    while not country:
        try:
            country = str(raw_input()) #Use pyCountry in the future
        except ValueError:
            print 'Invalid Country'
    return country

def post_csv():
    global CSV_FILE_NAME
    sftp = chilkat.CkSFtp()
    success = sftp.UnlockComponent("Anything for 30-day trial")
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    sftp.put_ConnectTimeoutMs(5000)
    sftp.put_IdleTimeoutMs(10000)

    hostname = "sftp://sftp.gdom.net"
    port = 22
    success = sftp.Connect(hostname,port)
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    success = sftp.AuthenticatePw("smellysocks","dai0xaeJ")
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    success = sftp.InitializeSftp()
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    handle = sftp.openFile(CSV_FILE_NAME,"writeOnly","createTruncate")
    if (sftp.get_LastMethodSuccess() != True):
        print(sftp.lastErrorText())
        sys.exit()

    #  Upload from the local file to the SSH server.
    success = sftp.UploadFile(handle,"./csv_library/" + CSV_FILE_NAME)
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    #  Close the file.
    success = sftp.CloseHandle(handle)
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    print("Success.")

def choose_path():
    print(sys_options)
    action = None
    while not action:
        try:
            action = int(raw_input())
        except ValueError:
            print('Invalid Number')

    if action == 1:
        run_experiment()
    else:
         if action == 2:
             clear()
             print('\n!!!!!!!!!! -- Option 2 has yet to be set up -- !!!!!!!!!!\n')
             choose_path()
         else:
            if action ==3:
                clear()
                print('\n!!!!!!!!!! -- Option 3 has yet to be set up -- !!!!!!!!!!\n')
                choose_path()
            else:
                if action == 4:
                    clear()
                    print('\n!!!!!!!!!! -- Option 4 has yet to be set up -- !!!!!!!!!!\n')
                    choose_path()
                else:
                    if action == 5:
                        clear()
                        print('\nGoodbye\n')
                        # print(mosquito)
                        sys.exit()
                    else:
                        if action == 6:
                                clear()
                                global SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, SOCK_OWNER_NAME_2, SOCK_OWNER_COUNTRY_2, CSV_FILE_NAME, CURRENT_DATE_TIME
                                SOCK_OWNER_NAME_1 = 'sockOwner1Name'
                                SOCK_OWNER_COUNTRY_1 = 'USA'
                                SOCK_OWNER_NAME_2 = 'sockOwner2Name'
                                SOCK_OWNER_COUNTRY_2 = 'FRANCE'
                                CSV_FILE_NAME = 'sockOwner1Name_VS_sockOwner2Name.csv'
                                CURRENT_DATE_TIME = str(datetime.datetime.now().strftime("%d-%m-%Y_%H:%M"))

                                print('Experiment Details:')
                                print(experiment_Details)
                                print('Test Chamber 1'.ljust(32, ' ') + SOCK_OWNER_NAME_1.ljust(32, ' ') + SOCK_OWNER_COUNTRY_1.ljust(32, ' ') + CSV_FILE_NAME.ljust(32, ' '))# + '000000007826'.ljust(32, ' ') + '\n')
                                print('Test Chamber 2'.ljust(32, ' ') + SOCK_OWNER_NAME_2.ljust(32, ' ') + SOCK_OWNER_COUNTRY_2.ljust(32, ' ') + CSV_FILE_NAME.ljust(32, ' '))# + '000000007827'.ljust(32, ' ') + '\n')
                                raw_input('\nConfirm information and prep Gates. Press <enter> to begin. \n ')

                                print(experiment_header)
                             ##   count_down('Open gates in', 5, '', False)
                                
                                
                                start_sensor_reader()
                                print(experiment_footer)

                                print('CSV saved to sockOwner1Name_VS_sockOwner2Name.csv\n\n')
                                myData = []
                                if yes_or_no('Rerun experiment? <y/n + enter>') == False:
                                    write_to_csv()
                                else:
                                    run_experiment()
def clear():
     os.system('cls' if os.name=='nt' else 'clear')

# ------------------------------------------------------------------------------------------------------
# Here begins the function calls.
# The program begins here:
#
clear()
print(welcome)
##time.sleep(4)
choose_path()