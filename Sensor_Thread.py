import threading
import time
import Sensor

exitFlag = 0
left = "not used yet"
right = "not used yet"
center = "not used yet"

def pline():
    global left, right, center
    print("|" + left.center(30, ' ') +
        "|".ljust(30, ' ') + "|" + right.center(30, ' ') +
        "|".ljust(30, ' ') + "|" + center.center(30, ' ') + "|")
            
class myThread (threading.Thread):
    
   def __init__(self, threadID, Sensor):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = Sensor.name
      self.Sensor = Sensor
            
   def run(self):
      t_end = time.time() + 60 * .01 #.5 is 30 seconds
      sensor = self.Sensor
      threadName = self.name
      global left, right, center
      
      threadLock.acquire()
      while time.time() < t_end:
##          print "%s: Reading(%s) at %s" % ( threadName, sensor.take_reading(), time.ctime(time.time()) )
          if exitFlag:
             threadName.exit()
          if(threadName == "left_decision_chamber"):
              if(sensor.take_reading() < (sensor.avg_voltage - .1)):
                left = "!!!DETECTED!!!"
                while((sensor.take_reading() < (sensor.avg_voltage)) and (time.time() < t_end)):
                 left = "-not counted-"
                else:           
                    left = str(sensor.take_reading())
                    
          if(threadName == "right_decision_chamber"):
              if(sensor.take_reading() < (sensor.avg_voltage - .01)):
                right = "!!!DETECTED!!!"
                while((sensor.take_reading() < (sensor.avg_voltage)) and (time.time() < t_end)):
                 right = "-not counted-"
              else:           
                right = str(sensor.take_reading())
          pline()
      threadLock.release()

left_dc_sensor = Sensor.init_sensor("left_decision_chamber","55739323237351310101")
right_dc_sensor = Sensor.init_sensor("right_decision_chamber",'5573932323735121C051')

threadLock = threading.Lock()
threads = []


# Create new threads
sensor1thread = myThread(1, left_dc_sensor)
sensor2thread = myThread(2, right_dc_sensor)

# Start new Threads
sensor1thread.start()
sensor2thread.start()

# Add threads to thread list
threads.append(sensor1thread)
threads.append(sensor2thread)

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"