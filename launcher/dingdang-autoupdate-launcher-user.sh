#!/bin/bash
sleep 1

# tmux session name
session_name="dingdang"

#Delete Cache
sudo rm -r $HOME/.cache
sudo rm -r $HOME/.netease-musicbox
sudo rm -r $HOME/userInfo
sleep 1

#AutoUpdate Before Launch
#Update dingdang-robot
cd $HOME/dingdang
git pull

#Update dingdang Requirements
sudo pip install --upgrade -r client/requirements.txt
sleep 1

#Update dingdang-contrib
cd $HOME/.dingdang/contrib
git pull

#Update dingdang-contrib Requirements
sudo pip install --upgrade -r requirements.txt
sleep 1

#Restore Configuration of AlsaMixer
if [ -f $HOME/asound.state ]; then
   alsactl --file=$HOME/asound.state restore
   sleep 1
fi

#Launch Dingdang in tmux
tmux new-session -d -s $session_name $HOME/dingdang/dingdang.py
sleep 1

#Start Respeaker-Switcher in Background
if [ -d $HOME/ReSpeaker-Switcher ]; then
    sudo python $HOME/ReSpeaker-Switcher/switcher.py &
fi

cd $HOME/dingdang
