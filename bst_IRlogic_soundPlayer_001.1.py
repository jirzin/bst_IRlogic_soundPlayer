""" This program scans activity on selected GPIO pins of RaspberryPi.
The acitivity is processed and program select and play back concrete
song from defined folder. Also it sends signal to selcted GPIO pins
that send signal to light dimmers. This program is written for interactive
instalation Taktovka placed in Musem of Bedrich Smetana in Prague.
This program is supposed to run on RaspberryPi model B+ extended by
custom made PCBs.

Author: Bastlit
"""
import os
import random """ just for testing purpouses """
import time

""""""""""""""""""""""" folder reading and sorting """""""""""""""""""""""

def sortListLenAlphabet(l):
    return sorted(sorted(l, key=len))

path = "bst_soundFolder/"
""" path variable stores path to folder containing tracks to be played """
absolutePath = '/home/ubu/bastlit/bedrich-smetana-taktovka/raspi_codes/bst_soundFolder/'

audioFiles = [f for f in os.listdir(absolutePath) if os.path.isfile(os.path.join(absolutePath,f))]
audioFiles = sortListLenAlphabet(audioFiles)
""" final sorted list of files in defined folder """


""" debugging print """
print "\nfolder to be read"
print path
print "\nfiles to be played"
print audioFiles

time.sleep(1)




""""""""""""""""""""""" GPIO pins definition """""""""""""""""""""""
""" order of pins selected according to PCB layout """
""" 12 input pins """
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
""" 10 output pins """
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



""""""""""""""""""""""" PIN LISTS & MAPS & SORTING FUNCTIONS """""""""""""""""""""""
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



""""""""""""""""""""""" APP VARS AND LOGIC HLEPERS """""""""""""""""""""""
""" helper selected vars  """
selectedInput = 0
selectedOutput = 0
selectedSong = ""

""" general program states"""
programStates = ["reading", "playing", "dimmingOut", "closing"]
programState = "reading"




""""""""""""""""""""""" GENERAL FUNCTIONS """""""""""""""""""""""
def pickSong (x):
    if x >= 0:
        song = audioFiles[x]
        print "\nplay file: " + song + '\n'
        time.sleep(0.5)
        os.system('mplayer ' + absolutePath + song)
        print "\nend of song\n"

    if x == -1:
        print "\nno track is selected\n"



def readInPinValues(inDict):
    n = 0
    keys = sortKeysLenAlphabet(inDict)
    for k in keys:
        print "id: " + str(k) + " value: " + str(inDict[k])


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


def changeSelectedSong(x, inDict):
    n = 0
    keys = sortKeysLenAlphabet(inDict)
    for k in keys:
        if n == x:
            inDict[k]=1
        else:
            inDict[k]=0
        n=n+1




""""""""""""""""""""""" MAIN LOOP """""""""""""""""""""""

while programState!="closing":

    if programState == "reading":
        changeSelectedSong(input("new song number: "),inPinValues)
        print '\n'
        readInPinValues(inPinValues)
        time.sleep(0.5)
        programState = "playing"

    if programState == "playing":
        pickSong(whichSong(inPinValues))
        time.sleep(1)
        programState = "dimmingOut"

    if programState == "dimmingOut":
        time.sleep(1)
        programState="reading"



print "zaviram aplikaci\n"
exit()
