#!/usr/bin/env python2
# -*- coding: utf-8-*-

import time
import os
from client.wxbot import WXBot

from client import dingdangpath
from client.tts import SimpleMp3Player
from client.audio_utils import mp3_to_wav


class WechatBot(WXBot):
    def __init__(self, brain):
        WXBot.__init__(self)
        self.brain = brain
        self.music_mode = None
        self.last = time.time()

    def handle_music_mode(self, msg_data):
        # avoid repeating command
        now = time.time()
        if (now - self.last) > 0.5:
            # stop passive listening
            # self.brain.mic.stopPassiveListen()
            self.last = now
            if not self.music_mode.delegating:
                self.music_mode.delegating = True
                self.music_mode.delegateInput(msg_data, True)
                if self.music_mode is not None:
                    self.music_mode.delegating = False

    def handle_msg_all(self, msg):
        # ignore the msg when handling plugins
        profile = self.brain.profile
        if (msg['msg_type_id'] == 1 and
           msg['to_user_id'] == self.my_account['UserName']):
            from_user = profile['first_name'] + '说：'
            if msg['content']['type'] == 0:
                msg_data = from_user + msg['content']['data']
                if msg_data.startswith(profile['robot_name_cn']+": "):
                    return
                if self.music_mode is not None:
                    return self.handle_music_mode(msg_data)
                self.brain.query([msg_data], self, True)
            elif msg['content']['type'] == 4:
                mp3_file = os.path.join(dingdangpath.TEMP_PATH,
                                        'voice_%s.mp3' % msg['msg_id'])
                # echo or command?
                if 'wechat_echo' in profile and not profile['wechat_echo']:
                    # 执行命令
                    mic = self.brain.mic
                    wav_file = mp3_to_wav(mp3_file)
                    with open(wav_file) as f:
                        command = mic.active_stt_engine.transcribe(f)
                        if command:
                            if self.music_mode is not None:
                                return self.handle_music_mode(msg_data)
                            self.brain.query(command, self, True)
                        else:
                            mic.say("什么？")
                else:
                    # 播放语音
                    player = SimpleMp3Player()
                    player.play_mp3(mp3_file)
        elif msg['msg_type_id'] == 4:
            if 'wechat_echo_text_friends' in profile and \
               (
                   msg['user']['name'] in profile['wechat_echo_text_friends']
                   or
                   'ALL' in profile['wechat_echo_text_friends']
               ) and msg['content']['type'] == 0:
                from_user = msg['user']['name'] + '说：'
                msg_data = from_user + msg['content']['data']
                self.brain.query([msg_data], self, True)
            elif 'wechat_echo_voice_friends' in profile and \
                 (
                    msg['user']['name'] in profile['wechat_echo_voice_friends']
                    or
                    'ALL' in profile['wechat_echo_voice_friends']
                 ) and msg['content']['type'] == 4:
                mp3_file = os.path.join(dingdangpath.TEMP_PATH,
                                        'voice_%s.mp3' % msg['msg_id'])
                player = SimpleMp3Player()
                player.play_mp3(mp3_file)
