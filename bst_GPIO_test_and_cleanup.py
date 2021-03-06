##############################################
# TESTING PROGRAM FOR RASPBERRY pi GPIO PINS #
##############################################

import time
import RPi.GPIO as GPIO

# PIN NUMBERING ACCORDING TO BCM CHIP ORDER
GPIO.setmode(GPIO.BCM)

# 12 INPUT PIN NUMBERS
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

# 10 OUTPUT PINS     
outPin1 =  27
outPin2 =  22
outPin3 =  10
outPin4 =  9
outPin5 =  11
outPin6 =  5
outPin7 =  6
outPin8 =  13
outPin9 =  19
outPin10 = 26

# PIN LISTS
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


##################
# GPIO PIN SETUP #
##################
for num in inPinList:
    GPIO.setup(num,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    time.sleep(0.1)

for num in outPinList:
    GPIO.setup(num,GPIO.OUT)
    GPIO.output(num,False)
    time.sleep(0.1)

#####################
# TESTING FUNCTIONS #
#####################
def blinkSequence(l, on, off, t):
    for i in range(t):
        for x in l:
            print "testig pin: " + str(x)
            GPIO.output(x,True)
            time.sleep(on)
            GPIO.output(x,False)
            time.sleep(off)


def setOutPinsOn(l):
    for x in l:
        GPIO.output(x,True)

def setOutPinsOff(l):
    for x in l:
        GPIO.output(x,False)

#######################################
# HERE IS PLACE FOR TESTING FUNCTIONS #
#######################################
#blinkSequence(outPinList,0.15,0.15,200)


# CLEANING
GPIO.cleanup()
exit()
