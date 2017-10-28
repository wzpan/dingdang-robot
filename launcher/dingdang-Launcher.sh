#!/bin/bash
sleep 1

#Delete Cache
sudo rm -r /root/.cache
sudo rm -r /root/.config
sudo rm -r /root/.netease-musicbox
sudo rm -r /root/userInfo

#Restore Configuration of AlsaMixer
alsactl --file=/home/pi/asound.state restore
sleep 1

#Start DingDang
sudo lxterminal -e "python /home/pi/dingdang/dingdang.py"
sleep 1
sudo python /home/pi/ReSpeaker-Switcher/switcher.py &
