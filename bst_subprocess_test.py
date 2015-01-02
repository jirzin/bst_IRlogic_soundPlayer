import os
import mpylayer
import subprocess
import time



print "this will open mplayer subprocess in 1 sec"
devnull = open('/dev/null','w')
player = subprocess.Popen(["mplayer", "/home/pi/bst_sounds/01_banibori_v_cechach.wav"],stdin=subprocess.PIPE,stdout=devnull,stderr=subprocess.PIPE)

time.sleep(1)
print "now you should hear some music"

time.sleep(1)



while True:

    time.sleep(0.02)

    if player.poll() is None:
        print "music is playing"
    else:
        print "music has stopped"
    

#player.wait()

print ("exitting")

exit()
