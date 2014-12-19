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
import random #""" just for testing purpouses """
import time
import RPi.GPIO as GPIO


# debugging print
print "\nGPIO version: " +GPIO.VERSION
time.sleep(1)
#exit()

#""""""""""""""""""""""" folder reading and sorting """""""""""""""""""""""

def sortListLenAlphabet(l):
    return sorted(sorted(l, key=len))

path = "/home/pi/bst_sounds/"
#""" path to folder containing tracks to be played """
absolutePath = '/home/pi/bst_sounds/'

audioFiles = [f for f in os.listdir(absolutePath) if os.path.isfile(os.path.join(absolutePath,f))]
audioFiles = sortListLenAlphabet(audioFiles)
#""" final sorted list of files in defined folder """


#""" debugging print """
#print "\nfolder to be read"
#print path
#print "\nfiles to be played"
#print audioFiles

time.sleep(1)

#""""""""""""""""""""""" GPIO and pins definition """""""""""""""""""""""
# GPIO general setup
GPIO.setmode(GPIO.BCM)

#""" order of pins selected according to PCB layout """
#""" 12 input pins """

# GPIO pin numbering for RaspberryPi B+
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


 
#""""""""""""""""""""""" PIN LISTS & MAPS & SORTING FUNCTIONS """""""""""""""""""""""
def sortKeysLenAlphabet(l):
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

for num in inPinList:
    print "setting pin " + str(num) + " as INPUT"
    GPIO.setup(num,GPIO.IN)
    time.sleep(0.2)


for num in outPinList:
    print "setting pin " + str(num) + " as OUTPUT"
    GPIO.setup(num,GPIO.OUT)
    time.sleep(0.2)

#while True:
for i in range(20):
    for num in outPinList:
        print "test " + str(num)
        GPIO.output(num,True)
        time.sleep(10)
        GPIO.output(num,False)
        time.sleep(10)


#time.sleep(100)

#print "testing complete"
#
#GPIO.cleanup()
#exit()

#time.sleep(1)

#for x in 

#while True:
#    for x in outPinList:
        


#""""""""""""""""""""""" ACCUMULATION OF ACTIVE PINS """"""""""""""""""""""
inPinAccum = {'inPin1':0, 'inPin2':0, 'inPin3':0,
              'inPin4':0, 'inPin5':0, 'inPin6':0,
              'inPin7':0, 'inPin8':0, 'inPin9':0,
              'inPin10':0, 'inPin11':0, 'inPin12':0
}

accumStep = 1;
accumMax = 255 # basically a time value needed for detector to be acceped focused one
readPeriod = 0.04
dimmThreshold = 100 # value of time needed for diimmer to start dimm


#""""""""""""""""""""""" APP VARS AND LOGIC HLEPERS """""""""""""""""""""""
#""" helper selected vars  """
selectedInput = 0
selectedOutput = 0
selectedSong = 0

#""" general program states"""
programStates = ["reading", "playing", "dimmingOut", "closing"]
programState = "reading"


#""""""""""""""""""""""" GENERAL FUNCTIONS """""""""""""""""""""""
#def pickSong (x):
#    if x >= 0:
#        song = audioFiles[x]
#        print "\nplay file: " + song + '\n'
#        time.sleep(0.5)
#        os.system('aplay ' + absolutePath + song)
#        print "\nend of song\n"
#
#    if x == -1:
#        print "\nno track is selected\n"



def readInPinValues(inList,inDict):
    n = 0
    keys = sortKeysLenAlphabet(inDict)
    for k in keys:
        inDict[k] = GPIO.input(inList[n])
        print "id: " + str(k) + " GPIO: " + str(inList[n]) + " value: " + str(inDict[k])
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

    keys = sortKeysLenAlphabet(inDict)
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
    keys = sortKeysLenAlphabet(accumDict)    
    for k in keys:
        ad = accumDict[k]
        # if one of detectors reach maximum value
        # return its order number
        # otherwise returns -1
        if ad == 255:
            return n        
        else:
            return -1
        # rise the order number
        n=n+1
    

def whichSong (vals):
    n = 0
    keys = sortKeysLenAlphabet(vals)
    for k in keys:
        if vals[k] == 0:
            n=n+1
        else:
            break
    if n >= len(keys):
        n = -1
    return n

def dimm(accum,out):
    n = 0
    keys = sortKeysLenAlphabet(accum)
    for k in keys:
        out[k] = 0
        if accum[k] > dimmThreshold:
            out[k] = 1

            
#def changeSelectedSong(x, inDict):
#    n = 0
#    keys = sortKeysLenAlphabet(inDict)
    # for k in keys:
    #     if n == x:
    #         inDict[k]=1
    #     else:
    #         inDict[k]=0
    #     n=n+1



#""""""""""""""""""""""" MAIN LOOP """""""""""""""""""""""

while programState!="closing":

    if programState == "reading":
        readInPinValues(inPinList,inPinValues)
#        accumInPinValues(inPinValues,inPinAccum)
#        dimm(inPinAccum,ouPinValues)
#        print "\n focused stand order: " + str(orderOfFocused(inPinAccum))
        time.sleep(readPeriod)
#        off = orderOfFocused(inPinAccum)
#        if off != -1:
#            selectedSong = off
#            programState = "playing"
            

    if programState == "playing":
        pickSong(whichSong(inPinValues))
        time.sleep(1)
        programState = "dimmingOut"

    if programState == "dimmingOut":
        time.sleep(1)
        programState="reading"



print "zaviram aplikaci\n"
exit()
