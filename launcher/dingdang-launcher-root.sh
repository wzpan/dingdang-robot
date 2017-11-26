#!/bin/bash
sleep 1

session_name=dingdang

#Delete Cache
sudo rm -r /root/.cache
sudo rm -r /root/.netease-musicbox
sudo rm -r /root/userInfo

#Restore Configuration of AlsaMixer
if [ -f $HOME/asound.state ]; then
    alsactl --file=$HOME/asound.state restore
    sleep 1
fi

#Start DingDang
sudo tmux new-session -d -s $session_name $HOME/dingdang/dingdang.py
sleep 1

if [ -d $HOME/ReSpeaker-Switcher ]; then
    python $HOME/ReSpeaker-Switcher/switcher.py &
fi

cd $HOME/dingdang
