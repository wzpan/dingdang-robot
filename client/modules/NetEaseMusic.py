# -*- coding: utf-8-*-
import logging
import threading
import hashlib
import time
import subprocess
import sys
import os
import random
sys.path.append('../')
import libs.NetEaseApi.api as NetEaseAPI

reload(sys)
sys.setdefaultencoding('utf8')

# Standard module stuff
WORDS = ["YINYUE"]

def handle(text, mic, profile):
    """
    Responds to user-input, typically speech text, by telling a joke.

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    logger = logging.getLogger(__name__)

    kwargs = {}
    kwargs['mic'] = mic
    if 'netease_music' in profile:
        if 'account' in profile['netease_music']:
            kwargs['account'] = profile['netease_music']['account']
        if 'password' in profile['netease_music']:
            kwargs['password'] = profile['netease_music']['password']

    logger.debug("Preparing to start netease music module")
    try:
        netease_wrapper = NetEaseWrapper(**kwargs)
    except:
        logger.error("Couldn't connect to NetEase server", exc_info=True)
        mic.say(u"访问网易云音乐失败了，请稍后再试")
        return    

    # FIXME: Make this configurable
    persona = 'DINGDANG'
    if 'robot_name' in profile:
        persona = profile['robot_name']

    logger.debug("Starting music mode")
    music_mode = MusicMode(persona, mic, netease_wrapper)
    music_mode.stop = False
    
    if any(word in text for word in [u"歌单", u"我的"]):
        music_mode.handleForever(1) # 1: 用户歌单
    else:
        # 默认播放推荐歌曲
        music_mode.handleForever(0) # 0: 推荐榜单
    logger.debug("Exiting music mode")

    return


def isValid(text):
    """
        Returns True if the input is related to jokes/humor.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in [u"听歌", u"音乐", u"播放", u"唱歌", u"唱首歌", u"歌单", u"榜单"])


# The interesting part
class MusicMode(object):

    def __init__(self, PERSONA, mic, netease_wrapper):
        self._logger = logging.getLogger(__name__)
        self.persona = PERSONA
        self.music = netease_wrapper
        self.mic = mic
        self.stop = False

    def delegateInput(self, input):
        
        command = input.upper()

        # check if input is meant to start the music module
        if u"榜单" in command:
            self.mic.say(u"播放榜单音乐")
            self.music.update_playlist_by_type(0)
            self.music.play()
            return
        elif u"歌单" in command:
            self.music.update_playlist_by_type(1)
            self.music.play()
            return
        elif any(ext in command for ext in [u"停止", u"结束"]):
            self.mic.say(u"停止播放")
            self.music.stop()
            return
        elif any(ext in command for ext in [u"播放", u"继续"]):
            self.music.play()
            return
        elif u"暂停" in command:
            self.mic.say(u"暂停播放")
            self.music.pause()
            return
        elif any(ext in command for ext in [u"大声", u"大声点", u"大点声"]):
            self.mic.say(u"大点声")
            self.music.increase_volume()
            self.music.play(False)
            return
        elif any(ext in command for ext in [u"小声", u"小点声", u"小声点"]):
            self.mic.say(u"小点声")
            self.music.decrease_volume()
            self.music.play(False)
            return
        elif any(ext in command for ext in [u'下一首', u"下首歌", u"切歌", u"下一首歌", u"一首歌", u"换首歌", u"切割", u"哥", u"那首歌"]):
            self.mic.say(u"下一首歌")
            self.music.next()
            self.music.play()
            return
        elif any(ext in command for ext in [u'上一首', u'上一首歌', u'上首歌']):
            self.mic.say(u"上一首歌")
            self.music.previous()            
            self.music.play()
            return
        elif u'随机' in command:
            self.mic.say(u"随机播放")
            self.music.randomize()
            self.music.play()
            return
        elif u'顺序' in command:
            self.mic.say(u"顺序播放")
            self.music.serialize()
            self.music.play()
            return
        elif u'退出' in command:
            self.mic.say(u"退出播放")
            self.music.stop()
            self.music.exit()
            return
        else:
            time.sleep(.5)
            self.mic.say(u"没有听懂呢。要退出播放，请说退出播放")
            self.music.play(False)
            return
        return

   
    def handleForever(self, play_type=0):
        """
        进入音乐播放
        play_type - 0：播放推荐榜单；1：播放用户歌单
        """

        self.music.update_playlist_by_type(play_type)        
        self.music.start() 

        while True:

            if self.stop:
                return

            threshold, transcribed = self.mic.passiveListen(self.persona)
            
            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue

            # 当听到呼叫机器人名字时，停止播放
            self.music.stop()
            time.sleep(.5)

            # 听用户说话
            input = self.mic.activeListen(MUSIC=True)

            if input:
                if any(ext in input for ext in ["结束", "退出"]):
                    time.sleep(.5)
                    self.mic.say(u"结束播放")
                    self.music.stop()                    
                    self.music.exit()
                    return
                self.delegateInput(input)
            else:
                self.mic.say(u"什么？")
                if not self.music.pause:
                    self.music.play(False)


class NetEaseWrapper(threading.Thread):

    def __init__(self, mic, account='', password=''):
        super(NetEaseWrapper, self).__init__()
        self.cond = threading.Condition() 
        self.netease = NetEaseAPI.NetEase()
        self.account = account
        self.password = password
        self.mic = mic
        self.userId = 33120312
        self.volume = 0.5
        self.song = None  # 正在播放的曲目信息
        self.idx = -1  # 正在播放的曲目序号
        self.random = False
        self.playlist = []

        
    def set_cond(self, cond):
        self.cond = cond

        
    def update_playlist_by_type(self, play_type):
        if play_type == 0:
            self.playlist = self.get_top_songlist()
        elif play_type == 1:
            has_login = False
            if not (os.path.exists('userInfo')):
                self.mic.say("稍等，正在为您登录网易云音乐")
                res = self.login(self.account, self.password)
                if res:
                    self.mic.say("登录成功")
                    has_login = True
            else:
                has_login = True                
            if has_login:
                user_playlist = self.get_user_playlist()
                if user_playlist > 0:
                    self.playlist = self.get_song_list_by_playlist_id(user_playlist[0]['id'])
                    if len(self.playlist) == 0:
                        self.mic.say("用户歌单没有歌曲，改为播放推荐榜单")
                        self.playlist = self.get_top_songlist()
                else:
                    self.mic.say("当前用户没有歌单，改为播放推荐榜单")
                    self.playlist = self.get_top_songlist()
            else:
                self.mic.say("登录失败，改为播放推荐榜单")
                self.playlist = self.get_top_songlist()




    def get_top_songlist(self):#热门单曲
        music_list = self.netease.top_songlist()
        datalist = self.netease.dig_info(music_list, 'songs')
        playlist = []
        for data in datalist:
            music_info = {}
            music_info.setdefault("song_name", data.get("song_name"))
            music_info.setdefault("artist", data.get("artist"))
            music_info.setdefault("album_name", data.get("album_name"))
            music_info.setdefault("mp3_url", data.get("mp3_url"))
            music_info.setdefault("playTime", data.get("playTime"))  # 音乐时长
            music_info.setdefault("quality", data.get("quality"))
            playlist.append(music_info)
        return playlist

    def login(self, username, password): #用户登陆
        password = hashlib.md5(password).hexdigest()
        login_info = self.netease.login(username, password)
        if login_info['code'] == 200:
            res = True
            userId = login_info.get('profile').get('userId')
            self.userId = userId
            file = open("./userInfo", 'w')
            file.write(str(userId))
            file.close()
        else:
            res = False
        return res

    def get_user_playlist(self):  #获取用户歌单
        play_list = self.netease.user_playlist(self.userId)  # 用户歌单
        return play_list

    def get_song_list_by_playlist_id(self, playlist_id):
        songs = self.netease.playlist_detail(playlist_id)
        song_list = self.netease.dig_info(songs, 'songs')
        return song_list

    def search_by_name(self, song_name):
        data = self.netease.search(song_name)
        song_ids = []
        if 'songs' in data['result']:
            if 'mp3Url' in data['result']['songs']:
                songs = data['result']['songs']

            else:
                for i in range(0, len(data['result']['songs'])):
                    song_ids.append(data['result']['songs'][i]['id'])
                songs = self.netease.songs_detail(song_ids)
        song_list = self.netease.dig_info(songs, 'songs')
        return song_list

    
    def current_song(self):
        if self.song != None:
            return self.song['song_name']
        else:
            return ''

    def run(self):
        while True:
            if self.cond.acquire():            
                self.play()
                self.next()
            
    def play(self, report=True):
        self.pause = False
        if self.idx < len(self.playlist):
            # 循环播放，取出第一首歌曲，放在最后的位置，类似一个循环队列
            if self.idx == -1:
                self.idx = 0
            if not self.random:
                song = self.playlist[self.idx]
            else:
                song = random.choice(self.playlist)
            self.song = song
            mp3_url = song["mp3_url"]
            try:
                subprocess.Popen("pkill play", shell=True)
                if report:
                    time.sleep(.5)
                    self.mic.say(u"即将播放 %s %s" % (song['artist'], song['song_name']))
                time.sleep(.5)
                subprocess.Popen("play -v %f %s"  % (self.volume, mp3_url), shell=True, stdout=subprocess.PIPE)
                self.cond.notify()
                self.cond.wait(int(song.get('playTime')) / 1000)
            except:
                pass
        else:
            try:
                subprocess.Popen("pkill play", shell=True)
                self.cond.notify()
                self.cond.wait()
            except:
                pass

    def notify(self):
        if self.cond.acquire():
            self.cond.notifyAll()
            self.cond.release()


    def previous(self):
        self.idx -= 1
        if self.idx < 0:
            self.idx = len(self.playlist) - 1
        self.notify()

    def next(self):
        self.idx += 1
        if self.idx > len(self.playlist) - 1:
            self.idx = 0
        self.notify()

    def randomize(self):
        self.random = True
        self.notify()

    def serialize(self):
        self.random = False
        self.notify()

    def increase_volume(self):
        self.volume += .1
        if self.volume > 1:
            self.volume = 1
        
    def decrease_volume(self):
        self.volume -= .1
        if self.volume < 0:
            self.volume = 0

    def stop(self):
        try:
            subprocess.Popen("pkill play", shell=True)
            self.cond.notify()
            self.cond.wait()
        except:
            pass

    def pause(self):
        self.pause = True
        # 暂不支持断点续播，因此暂停和停止相同处理
        self.stop()


    def exit(self):
        self.stop = True
        self.playlist = []
        self.notify()

        
