# -*- coding: utf-8-*-

import os
import shutil

WORDS = [u"HUANCUN"]
SLUG = "cleancache"
PRIORITY = 0


def handle(text, mic, profile, wxbot=None):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxBot -- wechat robot
    """
    temp = mic.dingdangpath.TEMP_PATH
    shutil.rmtree(temp)
    os.mkdir(temp)
    mic.say(u'缓存目录已清空', cache=True)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.lower() for word in ["清除缓存", u"清空缓存", u"清缓存"])
