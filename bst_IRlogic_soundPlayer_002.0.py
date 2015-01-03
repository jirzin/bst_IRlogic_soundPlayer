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
import subprocess

debug = True

if(debug):
    print "\nGPIO version: " +GPIO.VERSION
    time.sleep(1)
    #exit()

#######################
# SOUND RELATED STUFF #
#######################
def sortListLenAlphabet(l):
    return sorted(sorted(l, key=len))

path = "/home/pi/bst_sounds/"
absolutePath = '/home/pi/bst_sounds/'

audioFiles = [f for f in os.listdir(absolutePath) if os.path.isfile(os.path.join(absolutePath,f))]
audioFiles = sorted(audioFiles)

if(debug):
    print audioFiles
    #exit()

global player
player = MPlayerControl()

playerVolume = 100
playerVolumeStep = 1

############################
# GPIO SETUP MAPS AND VARS #
############################
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

def sortKeys(l):
    return sorted(sorted(l.keys()), key=len)

def setOutPinsOn(l):
    for x in l:
        GPIO.output(x,True)

def setOutPinsOff(l):
    for x in l:
        GPIO.output(x,False)

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

##################
# GPIO pin setup #
##################
for num in inPinList:
    print "setting pin " + str(num) + " as INPUT"
    GPIO.setup(num,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    time.sleep(0.2)

for num in outPinList:
    print "setting pin " + str(num) + " as OUTPUT"
    GPIO.setup(num,GPIO.OUT)
    GPIO.output(num,False)
    time.sleep(0.2)

inPinAccum = {'inPin1':0, 'inPin2':0, 'inPin3':0,
              'inPin4':0, 'inPin5':0, 'inPin6':0,
              'inPin7':0, 'inPin8':0, 'inPin9':0,
              'inPin10':0, 'inPin11':0, 'inPin12':0
}

############################
# GENERAL PROGRM VARIABLES #
############################

global selectedSong    # actually playing song
global soundIsPlaying  # reflect if sound is playing
global focusedStand    # actualy and temporalily focused stand
global selectedStand   # selected stand reflects actuall selected music
global accumStep       # speed of rise and fall slope
global accumMax        # maximal value of accumulation fro IR senzors
global readPeriod      # speed of reading GPIO pins

selectedSong = -1
soundIsPlaying = False
focusedStand = -1
selectedStand = -1
accumStep = 1
accumMax = 40
readPeriod = 0.04

#####################################
#   GENERAL FUNCTIONS DEFINITIONS   #
#####################################

def pickSong (x):
    song = absolutePath + audioFiles[x]
    return song

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
    #print '\n'
    keys = sortKeys(inDict)
    for k in keys:
        ad = accumDict[k]
        if inDict[k] == 1:
            ad = clamp(ad+accumStep,0,255)
        elif inDict[k] == 0:
            ad = clamp(ad-accumStep,0,255)
        # write accumulation to dictionary
        accumDict[k] = ad
        # print "id: " + str(k) + " accum: " + str(accumDict[k])

def orderOfFocused(accumDict):
    n = 0
    order = -1
    keys = sortKeys(accumDict)
    for k in keys:
        ad = accumDict[k]
        if ad > accumMax:
            order = n
        n=n+1
    return order

def clearAccumMap(accum):
    for k in accum.keys():
        accum[k] = 0

def blinkSequence(l, on, off, t):
    for i in range(t):
        for x in l:
            #print "testig pin: " + str(x)
            GPIO.output(x,True)
            time.sleep(on)
            GPIO.output(x,False)
            time.sleep(off)

def lightManager(inList,outList,playing):
    n = 0
    inKeys = sortKeys(inList)
    outKeys = sortKeys(outList)
    for inkey in inKeys:
        if n < 9:
            outkey = outKeys[n]
        else:
            outke = outKeys[9]

        if playing != n:
            outList[outkey] = inList[inkey]
        else:
            outList[outkey] = 1

        print "light for stand " + str(n) + ": " + str(outList[outkey])

        n = n + 1

    print "actually selected stand: " + str(playing)

def writeToGPIO(out,vals):
    n = 0
    keys = sortKeys(vals)
    # helper var for triple receiver case
    triada = False
    for key in keys:
        # normal stands with just one receiver
        if n < len(out)-1:
            #write results from receivers to lights
            GPIO.output(out[n],vals[key])
        # stand with three receivers
        else:
            # if any of three receivers detect signal
            # light on GPIO pin will be switched on
            if(vals[key]==1):
                triada = True
        n = n+1
    # write light output to triple receiver light
    GPIO.output(out[9],triada)


def soundManager(select):

    global soundIsPlaying
    global player
    global selectedSong

    if select != -1 :
        if soundIsPlaying:
            #print "sound is playing"
            if player.poll() is None:
                print "player is active"
                soundIsPlaying = True
           #     player.communicate('q')
            else:
                print "player is not active"
                soundIsPlaying = False

        else:
            #if select != selectedSong:
            selectedSong = select
            song = pickSong(select)
            print "starting mplayer subprocess"
            player.loadfile(song)
            player.volume = 100
            soundIsPlaying = True

    else:
        if soundIsPlaying :
            if player.poll() is None:
                print "player is active"

            else:
                print "player is not active"
                soundIsPlaying = False



##############
# MAIN LOOP  #
##############

while True:

    # if programState == "reading":

    readInPinValues(inPinList,inPinValues)
    accumInPinValues(inPinValues,inPinAccum)
    focusedStand = orderOfFocused(inPinAccum)

    if focusedStand > -1 :
        if selectedStand != focusedStand :
            selectedStand = focusedStand
    else:
        if soundIsPlaying:
            selectedStand = selectedStand
        else:
            selectedStand = -1

    lightManager(inPinValues,outPinValues,selectedStand)

    soundManager(selectedStand)

    time.sleep(readPeriod)




print "zaviram aplikaci\n"
exit()
