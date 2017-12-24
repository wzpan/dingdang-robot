# -*- coding: utf-8-*-
from sys import maxint
import random
from client.robot import get_robot_by_slug

WORDS = []
PRIORITY = -(maxint + 1)


def need_robot(profile):
    if 'robot' in profile and profile['robot'] is not None:
        return True
    return False


def handle(text, mic, profile, wxbot=None):
    """
    Reports that the user has unclear or unusable input.

    Arguments:
    text -- user-input, typically transcribed speech
    mic -- used to interact with the user (for both input and output)
    profile -- contains information related to the user (e.g., phone
               number)
    wxBot -- wechat robot
    """
    if need_robot(profile):
        slug = profile['robot']
        robot = get_robot_by_slug(slug)
        robot.get_instance(mic, profile, wxbot).chat(text)
    else:
        messages = [u"抱歉，您能再说一遍吗？",
                    u"听不清楚呢，可以再为我说一次吗？",
                    u"再说一遍好吗？"]
        message = random.choice(messages)
        mic.say(message, cache=True)


def isValid(text):
    return True
