Python music track player for RaspberryPi B+

Program can read values of the inputs, dimm the lights and play the song for currently selected music stand. The user can switch between the individual stands. Program is executed from bst_start.sh script in home folder of the user pi. This script is executed by cron software unitlity. Pyhton program si located in pi home directory. 

For track playback of sound we use the mpylayer python module.

input pin numbers according to BCM numbering: 
[14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]

output pin numbers according to BCM numbering:
[26, 19, 13, 6, 5, 11, 9, 10, 22, 27]

To modify program source you need to change the file /home/pi/bst_IRlogic_soundPlayer/bst_IRlogic_soundPlayer.002.py
To modify starting scritp you need to change /home/pi/bst_start.sh
To modify what should be started at boot time you need to change crontab file by command:
sudo crontab -e
