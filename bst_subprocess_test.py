import os
import mpylayer
import subprocess
import time
import random

global step
global stepMod
step = 0
stepMod = 25

global volume
volume = 100

print "this will open mplayer subprocess in 1 sec"
global devnull
devnull = open('/dev/null','w')

#global player
#player = subprocess.Popen(["mplayer","-volstep", "1", "-volume", "100",  "/home/ubu/bastlit/bedrich-smetana-taktovka/bst_sounds/01_branibori_v_cechach.wav"],stdin=subprocess.PIPE,stdout=devnull,stderr=subprocess.PIPE)
global player
global playerPosition

playerPosition = None

player = mpylayer.MPlayerControl()
path = "/home/ubu/bastlit/bedrich-smetana-taktovka/bst_sounds/"

songy = ["01_branibori_v_cechach.wav",
         "02_tajemstvi.wav",
         "03_certova_stena.wav"]

player.loadfile(path + random.choice(songy))
playerPosition = player.percent_pos
player.volume = 100

time.sleep(1)
print "now you should hear some music"

time.sleep(8)

def incmod(v,m):
    v += 1
    if v < 0:
        v = m-1
    if v >= m:
        v = 0
    return v

while True:
    step = incmod(step,stepMod)

    time.sleep(0.02)
#    print "length of loaded file: " + str(player.length)
#    print "actual position in file: "+ str(player.time_pos)
    print "percentage of position: "+str(playerPosition)


    if step == 0:
        playerPosition = player.percent_pos

    if volume > 0:
        print "volume down"
        volume -= 1
        player.volume = volume

    if volume <= 0 :
        print "loading new file"
        player.loadfile(path + random.choice(songy))
        volume = 100
        player.volume = volume
        for int in range(10):
            time.sleep(2)
            playerPosition = player.percent_pos
        #time.sleep(8)

#player.wait()

print ("exitting")

exit()
