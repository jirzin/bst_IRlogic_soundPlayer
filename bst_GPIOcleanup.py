import time
import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)

GPIO.setmode(GPIO.BCM)

inPin1 = 14
inPin2 = 15
inPin3 = 18
inPin4 = 23
inPin5 = 24
inPin6 = 25
inPin7 = 8
inPin8 = 7
inPin9 = 12
inPin10 = 16
inPin11 = 20
inPin12 = 21

#""" 10 output pins """
outPin1 = 26
outPin2 = 19
outPin3 = 13
outPin4 = 6
outPin5 = 5
outPin6 = 11
outPin7 = 9
outPin8 = 10
outPin9 = 22
outPin10 = 27


inPinList = [inPin1, inPin2, inPin3,
             inPin4, inPin5, inPin6,
             inPin7, inPin8, inPin9,
             inPin10, inPin11, inPin12
]

outPinList = [outPin1, outPin2, outPin3,
              outPin4, outPin5, outPin6,
              outPin7, outPin8, outPin9,
              outPin10
]

for num in inPinList:
#    print "setting pin " + str(num) + " as INPUT"
    GPIO.setup(num,GPIO.IN)
    time.sleep(0.1)


for num in outPinList:
#    print "setting pin " + str(num) + " as OUTPUT"
    GPIO.setup(num,GPIO.OUT)
#    GPIO.output(num,False)
    time.sleep(0.1)

GPIO.cleanup()
exit()
