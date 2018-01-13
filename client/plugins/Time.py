# -*- coding: utf-8-*-
import datetime
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = [u"TIME", u"SHIJIAN", u"JIDIAN"]
SLUG = "time"


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

    tz = getTimezone(profile)
    now = datetime.datetime.now(tz=tz)
    service = DateService()
    response = service.convertTime(now)
    if "AM" in response:
        response = u"上午" + response.replace("AM", "")
    elif "PM" in response:
        response = u"下午" + response.replace("PM", "")
    mic.say(u"现在时间是 %s " % response)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in ["时间", "几点"])
