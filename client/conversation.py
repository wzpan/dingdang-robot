# -*- coding: utf-8-*-
from __future__ import absolute_import
import logging
from .notifier import Notifier
from .brain import Brain
import time
from .drivers.pixels import pixels


class Conversation(object):

    def __init__(self, persona, mic, profile):
        self._logger = logging.getLogger(__name__)
        self.persona = persona
        self.mic = mic
        self.profile = profile
        self.brain = Brain(mic, profile)
        self.notifier = Notifier(profile, self.brain)
        self.wxbot = None

    def is_proper_time(self):
        """
        whether it's the proper time to gather
        notifications without disturb user
        """
        if 'do_not_bother' not in self.profile:
            return True
        else:
            if self.profile['do_not_bother']['enable']:
                if 'since' not in self.profile['do_not_bother'] or \
                   'till' not in self.profile['do_not_bother']:
                    return True
                else:
                    since = self.profile['do_not_bother']['since']
                    till = self.profile['do_not_bother']['till']
                    current = time.localtime(time.time()).tm_hour
                    if till > since:
                        return current not in range(since, till)
                    else:
                        return not (current in range(since, 25) or
                                    current in range(-1, till))
            else:
                return True

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'.",
                          self.persona)
        while True:
            # Print notifications until empty
            if self.is_proper_time():
                notifications = self.notifier.getAllNotifications()
                for notif in notifications:
                    self._logger.info("Received notification: '%s'",
                                      str(notif))
                    self.mic.say(str(notif))

            if self.mic.stop_passive:
                self._logger.info("skip conversation for now.")
                time.sleep(1)
                continue

            if not self.mic.skip_passive:
                self._logger.debug("Started listening for keyword '%s'",
                                   self.persona)
                threshold, transcribed = self.mic.passiveListen(self.persona)
                self._logger.debug("Stopped listening for keyword '%s'",
                                   self.persona)

                if not transcribed or not threshold:
                    self._logger.info("Nothing has been said or transcribed.")
                    continue
                self._logger.info("Keyword '%s' has been said!", self.persona)
            else:
                self._logger.debug("Skip passive listening")
                if not self.mic.chatting_mode:
                    self.mic.skip_passive = False
            pixels.wakeup()
            self._logger.debug("Started to listen actively with threshold: %r",
                               threshold)
            input = self.mic.activeListenToAllOptions(threshold)
            self._logger.debug("Stopped to listen actively with threshold: %r",
                               threshold)
            pixels.think()
            if input:
                self.brain.query(input, self.wxbot)
            else:
                self.mic.say("什么?")
            pixels.off()
