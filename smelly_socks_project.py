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
import serial.tools.list_ports
from struct import unpack
from binascii import unhexlify
import Sensor
import SFTP_Client as sftp

#default vairables
SOCK_OWNER_NAME_1 = 'no_name_entered'
SOCK_OWNER_COUNTRY_1 = 'no_country_entered'
SOCK_OWNER_NAME_2 = 'no_name_entered'
SOCK_OWNER_COUNTRY_2 = 'no_country_entered'
CURRENT_DATE_TIME = 'system_date_error'
CSV_FILE_NAME = 'no_csv_name_assigned'

RELEASE_CHAMBER_COUNT = 0
LEFT_CHAMBER_COUNT = 0
RIGHT_CHAMBER_COUNT = 0
RESPONCE_RATE = 0.00
LEFT_ATTRACTANT_RATE = 0.00
RIGHT_ATTRACTANT_RATE = 0.00


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
2) Adjust Sensors
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

    if yes_or_no('Rerun experiment? <y/n + enter>') == False:
        write_to_csv()
    else:
        run_experiment()

##def write_to_csv():
##    global SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, SOCK_OWNER_NAME_2, SOCK_OWNER_COUNTRY_2, CSV_FILE_NAME, CURRENT_DATE_TIME, RESPONCE_RATE
##    DATA_COLLECTED = [[SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, CURRENT_DATE_TIME, str(RESPONCE_RATE)],[SOCK_OWNER_NAME_2, SOCK_OWNER_COUNTRY_2, CURRENT_DATE_TIME, str(RESPONCE_RATE)]] #Delete when real data is hereDATA_COLLECTED = [[SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, CURRENT_DATE_TIME, SOCK_OWNER_NAME_2, SOCK_OWNER_COUNTRY_2, counter]]
##    data = {SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, CURRENT_DATE_TIME, str(RESPONCE_RATE)}
##    csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
##    csv_file = open("./csv_library/Smelly_Socks_Database.csv", 'a')
##    with csv_file:
##        writer = csv.writer(csv_file, dialect = 'myDialect')
##        for line in DATA_COLLECTED:
##            writer.writerows([[line]])
##    clear()
##    sftp.post_csv()
##    print(experiment_summary_and_re_prompt)
##    # print(sys_options)
##    choose_path()

def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Please enter either y or n")
    
def calculate_stats():
    global RELEASE_CHAMBER_COUNT, LEFT_CHAMBER_COUNT, RIGHT_CHAMBER_COUNT, RESPONCE_RATE, LEFT_ATTRACTANT_RATE, RIGHT_ATTRACTANT_RATE
    
    RESPONCE_RATE = ((RELEASE_CHAMBER_COUNT/25.00) * 100.0)
    LEFT_ATTRACTANT_RATE = ((LEFT_CHAMBER_COUNT/25.00) * 100.0)
    RIGHT_ATTRACTANT_RATE = ((RIGHT_CHAMBER_COUNT/25.00) * 100.0)
    
    print("Release Chamber Sensor:".ljust(32, ' ') + "Left Decision Chamber Sensor:".center(40, ' ') + "Right Desicion Chamber Sensor:".rjust(40, ' '))
    print('Mosqutioes Counted: {}'.ljust(38, ' ').format(RELEASE_CHAMBER_COUNT) + 'Mosqutioes Counted: {}'.ljust(46, ' ').format(LEFT_CHAMBER_COUNT) + 'Mosqutioes Counted: {}'.ljust(40, ' ').format(RIGHT_CHAMBER_COUNT))# + '000000007826'.ljust(32, ' ') + '\n')
    print('Responce Rate: {}/25 = {}%'.ljust(38, ' ').format(RELEASE_CHAMBER_COUNT, RESPONCE_RATE) +
          'Attractant Rate: {}/25 = {}%'.ljust(46, ' ').format(LEFT_CHAMBER_COUNT, LEFT_ATTRACTANT_RATE) +
          'Attractant Rate: {}/25 = {}%'.ljust(40, ' ').format(RIGHT_CHAMBER_COUNT, RIGHT_ATTRACTANT_RATE))
    
    
def pline(left,right,center):
            print("| Release Chamber: " + str(left).center(15, ' ') +
              "|".ljust(15, ' ') + "|  Left Decision Chamber: " + str(right).center(15, ' ') +
              "|".ljust(15, ' ') + "| Right Decision Chamber: " + str(center).center(15, ' ') + "|")

def start_sensor_reader():
    
    global RELEASE_CHAMBER_COUNT, LEFT_CHAMBER_COUNT, RIGHT_CHAMBER_COUNT
    RELEASE_CHAMBER_COUNT = 0
    LEFT_CHAMBER_COUNT = 0
    RIGHT_CHAMBER_COUNT = 0
    
    left_dc_sensor = Sensor.init_sensor("left_decision_chamber","55739323237351D091A1")
    right_dc_sensor = Sensor.init_sensor("right_decision_chamber",'5573932323735121C051')
    release_c_sensor = Sensor.init_sensor("release_chamber",'55739323237351310101')
    
    
    count_down('Open gates in', 5, '', False) #delete after demo EXPERIMENT_PREP_TIME
    t_end = time.time() + 60 * .5 #.5 is 30 seconds
    print(experiment_header)
    print("TEST HAS BEGUN")
    
    left_dc_voltage = 0.00
    right_dc_voltage = 0.00
    release_chamber_voltage = 0.00

    
    
    while time.time() <= t_end:
        if(left_dc_sensor.take_reading() < (left_dc_sensor.avg_voltage - 0.03)):
           LEFT_CHAMBER_COUNT += 1
           pline("!!!DETECTED!!!", right_dc_sensor.take_reading(),release_c_sensor.take_reading())
           while(((left_dc_sensor.take_reading()) < (left_dc_sensor.avg_voltage - 0.03)) and (time.time() <= t_end)):
              pline("- not counted -", right_dc_sensor.take_reading(),release_c_sensor.take_reading())
                    
        if(right_dc_sensor.take_reading() < (right_dc_sensor.avg_voltage - 0.03)):
           RIGHT_CHAMBER_COUNT += 1
           pline(left_dc_sensor.take_reading(),"!!!DETECTED!!!", release_c_sensor.take_reading())
           while((right_dc_sensor.take_reading() < (right_dc_sensor.avg_voltage - 0.03)) and (time.time() <= t_end)):
              pline(left_dc_sensor.take_reading(),"- not counted -",release_c_sensor.take_reading())

        if(release_c_sensor.take_reading() < (release_c_sensor.avg_voltage - 0.03)):
           RELEASE_CHAMBER_COUNT +=1
           pline(left_dc_sensor.take_reading(), right_dc_sensor.take_reading(),("!!!DETECTED!!!" + str(release_c_sensor.voltage)))
           while((release_c_sensor.take_reading() < (release_c_sensor.avg_voltage - 0.03)) and (time.time() <= t_end)):
              pline(left_dc_sensor.take_reading(),right_dc_sensor.take_reading(), "- not counted -")

        pline(left_dc_sensor.take_reading(),right_dc_sensor.take_reading() ,release_c_sensor.take_reading())      
    

    print("!!!!!!!!!!!!!!DONE!!!!!!!!!!!!!!\n")
    calculate_stats()

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

    
def adjust_sensors():
    left_dc_sensor = Sensor.init_sensor("left_decision_chamber","55739323237351310101")
    right_dc_sensor = Sensor.init_sensor("right_decision_chamber",'5573932323735121C051')
    release_c_sensor = Sensor.init_sensor("release_chamber",'55739323237351D091A1')
    
    try:
        while True:
            pline(left_dc_sensor.take_reading(),right_dc_sensor.take_reading() ,release_c_sensor.take_reading())
    except KeyboardInterrupt:
        choose_path()

       
       
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
             print("You have selected to adjust the sensor. Press the spacebar when finished.")
             adjust_sensors()
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
                               
##                                print(experiment_header)
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
#write_to_csv()
print(welcome)
##time.sleep(4)
choose_path()