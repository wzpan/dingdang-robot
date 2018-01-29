# -*- coding: utf-8-*-
from __future__ import print_function
from __future__ import absolute_import
import requests
import json
import logging
from uuid import getnode as get_mac
from .app_utils import sendToUser, create_reminder
from abc import ABCMeta, abstractmethod

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class AbstractRobot(object):

    __metaclass__ = ABCMeta

    @classmethod
    def get_instance(cls, mic, profile, wxbot=None):
        instance = cls(mic, profile, wxbot)
        cls.mic = mic
        cls.wxbot = wxbot
        return instance

    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)

    @abstractmethod
    def chat(self, texts):
        pass


class TulingRobot(AbstractRobot):

    SLUG = "tuling"

    def __init__(self, mic, profile, wxbot=None):
        """
        图灵机器人
        """
        super(self.__class__, self).__init__()
        self.mic = mic
        self.profile = profile
        self.wxbot = wxbot
        self.tuling_key = self.get_key()

    def get_key(self):
        if 'tuling' in self.profile:
            if 'tuling_key' in self.profile['tuling']:
                tuling_key = \
                        self.profile['tuling']['tuling_key']
        return tuling_key

    def chat(self, texts):
        """
        使用图灵机器人聊天

        Arguments:
        texts -- user input, typically speech, to be parsed by a module
        """
        msg = ''.join(texts)
        try:
            url = "http://www.tuling123.com/openapi/api"
            userid = str(get_mac())[:32]
            body = {'key': self.tuling_key, 'info': msg, 'userid': userid}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
                result = result.replace(u'\xa0', u' ')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " +\
                             k['article'] + "\t" + k['detailurl'] + "\n"
            else:
                result = respond['text'].replace('<br>', '  ')
                result = result.replace(u'\xa0', u' ')
            max_length = 200
            if 'max_length' in self.profile:
                max_length = self.profile['max_length']
            if len(result) > max_length and \
               self.profile['read_long_content'] is not None and \
               not self.profile['read_long_content']:
                target = '邮件'
                if self.wxbot is not None and self.wxbot.my_account != {} \
                   and not self.profile['prefers_email']:
                    target = '微信'
                self.mic.say(u'一言难尽啊，我给您发%s吧' % target, cache=True)
                if sendToUser(self.profile, self.wxbot, u'回答%s' % msg, result):
                    self.mic.say(u'%s发送成功！' % target, cache=True)
                else:
                    self.mic.say(u'抱歉，%s发送失败了！' % target, cache=True)
            else:
                self.mic.say(result, cache=True)
            if result.endswith('?') or result.endswith(u'？') or \
               u'告诉我' in result or u'请回答' in result:
                self.mic.skip_passive = True
        except Exception:
            self._logger.critical("Tuling robot failed to responsed for %r",
                                  msg, exc_info=True)
            self.mic.say("抱歉, 我的大脑短路了 " +
                         "请稍后再试试.", cache=True)


class Emotibot(AbstractRobot):

    SLUG = "emotibot"

    def __init__(self, mic, profile, wxbot=None):
        """
        Emotibot机器人
        """
        super(self.__class__, self).__init__()
        self.mic = mic
        self.profile = profile
        self.wxbot = wxbot
        (self.appid, self.location, self.more) = self.get_config()

    def get_config(self):
        if 'emotibot' in self.profile:
            if 'appid' in self.profile['emotibot']:
                appid = \
                        self.profile['emotibot']['appid']
            if 'location' in self.profile:
                location = \
                        self.profile['location']
            else:
                location = None
            if 'active_mode' in self.profile['emotibot']:
                more = \
                        self.profile['emotibot']['active_mode']
            else:
                more = False
        return (appid, location, more)

    def chat(self, texts):
        """
        使用Emotibot机器人聊天

        Arguments:
        texts -- user input, typically speech, to be parsed by a module
        """
        msg = ''.join(texts)
        try:
            url = "http://idc.emotibot.com/api/ApiKey/openapi.php"
            userid = str(get_mac())[:32]
            register_data = {
                "cmd": "chat",
                "appid": self.appid,
                "userid": userid,
                "text": msg,
                "location": self.location
            }
            r = requests.post(url, params=register_data)
            jsondata = json.loads(r.text)
            result = ''
            responds = []
            if jsondata['return'] == 0:
                if self.more:
                    datas = jsondata.get('data')
                    for data in datas:
                        responds.append(data.get('value'))
                else:
                    responds.append(jsondata.get('data')[0].get('value'))
                result = '\n'.join(responds)

                if jsondata.get('data')[0]['cmd'] == 'reminder':
                    data = jsondata.get('data')[0]
                    remind_info = data.get('data').get('remind_info')
                    remind_event = remind_info[0].get('remind_event')
                    remind_time = remind_info[0].get('remind_time')

                    if not create_reminder(remind_event, remind_time):
                        result = u'创建提醒失败了'
            else:
                result = u"抱歉, 我的大脑短路了，请稍后再试试."
            max_length = 200
            if 'max_length' in self.profile:
                max_length = self.profile['max_length']
            if len(result) > max_length and \
               self.profile['read_long_content'] is not None and \
               not self.profile['read_long_content']:
                target = '邮件'
                if self.wxbot is not None and self.wxbot.my_account != {} \
                   and not self.profile['prefers_email']:
                    target = '微信'
                self.mic.say(u'一言难尽啊，我给您发%s吧' % target, cache=True)
                if sendToUser(self.profile, self.wxbot, u'回答%s' % msg, result):
                    self.mic.say(u'%s发送成功！' % target, cache=True)
                else:
                    self.mic.say(u'抱歉，%s发送失败了！' % target, cache=True)
            else:
                self.mic.say(result, cache=True)
            if result.endswith('?') or result.endswith(u'？') or \
               u'告诉我' in result or u'请回答' in result:
                self.mic.skip_passive = True

        except Exception:
            self._logger.critical("Emotibot failed to responsed for %r",
                                  msg, exc_info=True)
            self.mic.say("抱歉, 我的大脑短路了 " +
                         "请稍后再试试.", cache=True)


def get_robot_by_slug(slug):
    """
    Returns:
        A robot implementation available on the current platform
    """
    if not slug or type(slug) is not str:
        raise TypeError("Invalid slug '%s'", slug)

    selected_robots = filter(lambda robot: hasattr(robot, "SLUG") and
                             robot.SLUG == slug, get_robots())
    if len(selected_robots) == 0:
        raise ValueError("No robot found for slug '%s'" % slug)
    else:
        if len(selected_robots) > 1:
            print("WARNING: Multiple robots found for slug '%s'. " +
                  "This is most certainly a bug." % slug)
        robot = selected_robots[0]
        return robot


def get_robots():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [robot for robot in
            list(get_subclasses(AbstractRobot))
            if hasattr(robot, 'SLUG') and robot.SLUG]
