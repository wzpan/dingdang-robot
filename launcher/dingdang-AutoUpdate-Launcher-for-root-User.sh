#!/bin/bash
sleep 1

#Delete Cache
sudo rm -r /root/.cache
sudo rm -r /root/.config
sudo rm -r /root/.netease-musicbox
sudo rm -r /root/userInfo
sleep 1

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
sudo lxterminal -e "python /home/pi/dingdang/dingdang.py"
sleep 1

#Start Respeaker-Switcher in Background
sudo python /home/pi/ReSpeaker-Switcher/switcher.py &
