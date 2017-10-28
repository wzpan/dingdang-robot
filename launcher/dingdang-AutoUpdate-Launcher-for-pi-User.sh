#!/bin/bash
sleep 1

#Delete Cache
sudo rm -r /home/pi/.cache
sudo rm -r /home/pi/.config
sudo rm -r /home/pi/.netease-musicbox
sudo rm -r /home/pi/userInfo
sleep 1

#AutoUpdate Before Launch
#Update dingdang-robot
cd /home/pi/dingdang
git pull

#Update dingdang-contrib
cd /home/pi/.dingdang/contrib
git pull

#Update dingdang-contrib Requirements
sudo pip install --upgrade -r requirements.txt
sleep 1

#Restore Configuration of AlsaMixer
alsactl --file=/home/pi/asound.state restore
sleep 1

#Launch Dingdang in LxTerminal
lxterminal -e "python /home/pi/dingdang/dingdang.py"
sleep 1

#Start Respeaker-Switcher in Background
sudo python /home/pi/ReSpeaker-Switcher/switcher.py &
