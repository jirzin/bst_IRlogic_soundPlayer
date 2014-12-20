# This program scans activity on selected GPIO pins of RaspberryPi.
# The acitivity is processed and program select and play back concrete
# song from defined folder. Also it sends signal to selcted GPIO pins
# that control light dimmers. This program is written for interactive
# instalation Taktovka placed in Musem of Bedrich Smetana in Prague.
# This program is supposed to run on RaspberryPi model B+ extended by
# custom made PCBs.
#
# Author: Bastlit

import os
import random # just for testing purpouses
import time
import RPi.GPIO as GPIO


# debugging print
print "\nGPIO version: " +GPIO.VERSION
time.sleep(1)
#exit()

# folder reading and sorting

def sortListLenAlphabet(l):
    return sorted(sorted(l, key=len))



path = "/home/pi/bst_sounds/"
# path to folder containing tracks to be played
absolutePath = '/home/pi/bst_sounds/'

audioFiles = [f for f in os.listdir(absolutePath) if os.path.isfile(os.path.join(absolutePath,f))]
audioFiles = sorted(sorted(audioFiles),key=len)
# final sorted list of files in defined folder

#print audioFiles
#exit()

# GPIO and pins definition
# GPIO general setup
GPIO.setmode(GPIO.BCM)

# order of pins selected according to PCB layout
# GPIO pin numbering for RaspberryPi B+
# 12 input pins

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

# 10 output pins 
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

 
# PIN LISTS & MAPS & SORTING FUNCTIONS
def sortKeys(l):
    return sorted(sorted(l.keys()), key=len)



inPinList = [inPin1, inPin2, inPin3,
             inPin4, inPin5, inPin6,
             inPin7, inPin8, inPin9,
             inPin10, inPin11, inPin12
]


inPinValues = {'inPin1':0, 'inPin2':0, 'inPin3':0,
               'inPin4':0, 'inPin5':0, 'inPin6':0,
               'inPin7':0, 'inPin8':0, 'inPin9':0,
               'inPin10':0, 'inPin11':0, 'inPin12':0
}

#print sortKeys(inPinValues)
#exit()

outPinList = [outPin1, outPin2, outPin3,
              outPin4, outPin5, outPin6,
              outPin7, outPin8, outPin9,
              outPin10
]

outPinValues = {'outPin1':0, 'outPin2':0, 'outPin3':0,
                'outPin4':0, 'outPin5':0, 'outPin6':0,
                'outPin7':0, 'outPin8':0, 'outPin9':0,
                'outPin10':0
}

# general GPIO pin setup
for num in inPinList:
    print "setting pin " + str(num) + " as INPUT"
    GPIO.setup(num,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    time.sleep(0.2)

# default value for output is False = 0V 
for num in outPinList:
    print "setting pin " + str(num) + " as OUTPUT"
    GPIO.setup(num,GPIO.OUT)
    GPIO.output(num,False)
    time.sleep(0.2)
        
# ACCUMULATION OF ACTIVE PINS 
inPinAccum = {'inPin1':0, 'inPin2':0, 'inPin3':0,
              'inPin4':0, 'inPin5':0, 'inPin6':0,
              'inPin7':0, 'inPin8':0, 'inPin9':0,
              'inPin10':0, 'inPin11':0, 'inPin12':0
}


# APP VARS AND LOGIC HLEPERS
# helper selected vars  
selectedInput = 0
selectedOutput = 0
selectedSong = 0

accumStep = 1 # rise and fall speed of accumulated value
accumMax = 40 # basically a time value needed for detector to be acceped as focused

readPeriod = 0.04 

# general program states
programStates = ["reading", "playing", "dimmingOut", "closing"]
programState = "reading"

#  GENERAL FUNCTIONS  
def pickSong (x):    
    song = audioFiles[x]
    print "\nplay file: " + song + '\n'
    time.sleep(0.5)
    os.system('aplay ' + absolutePath + song)
    print "\nend of song\n"

def readInPinValues(inList,inDict):
    n = 0
    keys = sortKeys(inDict)
    for k in keys:
        inDict[k] = GPIO.input(inList[n])
        n = n+1        

def clamp(x,minim,maxim):
    if x < minim:
        return minim
    elif x > maxim:
        return maxim
    else:
        return x


def accumInPinValues(inDict,accumDict):
    print '\n'

    keys = sortKeys(inDict)
    for k in keys:
        ad = accumDict[k]
        if inDict[k] == 1:
            ad = clamp(ad+accumStep,0,255)
        elif inDict[k] == 0:
            ad = clamp(ad-accumStep,0,255)
        # write accumulation to dictionary
        accumDict[k] = ad
        print "id: " + str(k) + " accum: " + str(accumDict[k])


def orderOfFocused(accumDict):
    n = 0
    order = -1
    keys = sortKeys(accumDict)    
    for k in keys:
        ad = accumDict[k]
        if(ad>accumMax):
            order = n
        n=n+1
    return order

def whichSong (vals):
    n = 0
    keys = sortKeys(vals)
    for k in keys:
        if vals[k] == 0:
            n=n+1
        else:
            break
    if n >= len(keys):
        n = -1
    return n

def clearAccumMap(accum):
    for k in accum.keys():
        accum[k] = 0

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


def testTaktovka(out,vals):
    n = 0
    keys = sortKeys(vals)
    # helper var for triple receiver stand
    triada = False
    for key in keys:
        # normal stands with just one receiver
        if n < len(out)-1:
            #write results from receivers to lights
            GPIO.output(out[n],vals[key])
        # stand with three receivers
        else:
            if(vals[key]==1):
                triada = True
        n = n+1
    # write light output to triple receiver light
    GPIO.output(out[8],triada)

#def setLight(accum):
    
    

            
#def changeSelectedSong(x, inDict):
#    n = 0
#    keys = sortKeys(inDict)
    # for k in keys:
    #     if n == x:
    #         inDict[k]=1
    #     else:
    #         inDict[k]=0
    #     n=n+1



# MAIN LOOP 

while programState!="closing":

    if programState == "reading":
        readInPinValues(inPinList,inPinValues)
        testTaktovka(outPinList,inPinValues)
        accumInPinValues(inPinValues,inPinAccum)
        foc = orderOfFocused(inPinAccum) 
        print "order of focused: " + str(foc)
        if foc != -1:
            programState = "playing"
            selectedTrack = foc
        time.sleep(readPeriod)
#        off = orderOfFocused(inPinAccum)
#        if off != -1:
#            selectedSong = off
#            programState = "playing"
            

    if programState == "playing":
        clearAccumMap(inPinAccum)
        pickSong(selectedSong)
        time.sleep(1)
        programState = "dimmingOut"

    if programState == "dimmingOut":
        setOutPinsOff(outPinList)
        time.sleep(3)
        programState="reading"



print "zaviram aplikaci\n"
exit()
