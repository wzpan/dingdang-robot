#!/bin/bash
sleep 1

#Delete Cache
sudo rm -r /root/.cache
sudo rm -r /root/.netease-musicbox
sudo rm -r /root/userInfo

#Restore Configuration of AlsaMixer
if [ -f /home/pi/asound.state ]; then
    alsactl --file=/home/pi/asound.state restore
    sleep 1
fi

#Start DingDang
sudo tmux new-session -d -s $session_name $HOME/dingdang/dingdang.py
sleep 1

if [ -d /home/pi/ReSpeaker-Switcher]; then
    sudo python /home/pi/ReSpeaker-Switcher/switcher.py &
fi
