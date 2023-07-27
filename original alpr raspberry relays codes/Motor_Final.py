import sys
import time
import RPi.GPIO as GPIO
import Distance_Snsr

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24

StepPins = [17,22,23,24] # this is raspberry pi GPIO pins

# Set all pins as output
for pin in StepPins:
  print("Setup pins")
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
# This is motor steps
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]

StepCount = len(Seq)
StepDir = 1 # Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise

# Read wait time from command line
if len(sys.argv)>1:
  WaitTime = int(sys.argv[1])/float(1000)
else:
  WaitTime = 1/float(1000)

# Initialise variables
StepCounter = 0

# Start main loop

def MoveForward(StepCounter,StepDir,Step):

    while True:

      #print (StepCounter,)
      #print (Seq[StepCounter])

      for pin in range(0, 4):
        xpin = StepPins[pin]#
        if Seq[StepCounter][pin]!=0:
          print (" Enable GPIO %i" %(xpin))
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)

def MoveMotor(StepCounter,StepDir,Step):
    ct=0

    while True:
      if ct>Step:
       break
      #print (StepCounter,)
      #print (Seq[StepCounter])

      for pin in range(0, 4):
        xpin = StepPins[pin]#
        if Seq[StepCounter][pin]!=0:
          #print (" Enable GPIO %i" %(xpin))
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)
      ct+=1
      StepCounter += StepDir

      # If we reach the end of the sequence
      # start again
      if (StepCounter>=StepCount):
        StepCounter = 0
      if (StepCounter<0):
        StepCounter = StepCount+StepDir

      # Wait before moving on
      time.sleep(WaitTime)

def StepForward(StepCounter,Step):
    MoveMotor(StepCounter,1,Step)

def StepBackward(StepCounter,Step):

    MoveMotor(StepCounter,-1,Step)

#*********************** For motor movement
def open():
    motorSteps=1800 # steps

    StepForward(StepCounter,motorSteps)
    time.sleep(3)

    dist = Distance_Snsr.distance()

    if dist<8:
      dist = Distance_Snsr.distance()
      print("Measured Distance in motor = %.1f cm" % dist)
      while True:
        time.sleep(1)
        d1 = Distance_Snsr.distance()
        if d1>8:
         break
        print(" Distance is still in motor = %.1f cm" % dist)

    StepBackward(StepCounter,motorSteps)