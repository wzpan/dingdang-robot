# -*- coding: utf-8-*-
from __future__ import absolute_import
import Queue
import atexit
from .plugins import Email
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from . import app_utils
import time


class Notifier(object):

    class NotificationClient(object):

        def __init__(self, gather, timestamp):
            self.gather = gather
            self.timestamp = timestamp

        def run(self):
            self.timestamp = self.gather(self.timestamp)

    def __init__(self, profile, brain):
        self._logger = logging.getLogger(__name__)
        self.q = Queue.Queue()
        self.profile = profile
        self.notifiers = []
        self.brain = brain

        if 'email' in profile and \
           ('enable' not in profile['email'] or profile['email']['enable']):
            self.notifiers.append(self.NotificationClient(
                self.handleEmailNotifications, None))
        else:
            self._logger.debug('email account not set ' +
                               'in profile, email notifier will not be used')

        if 'robot' in profile and profile['robot'] == 'emotibot':
            self.notifiers.append(self.NotificationClient(
                self.handleRemenderNotifications, None))

        sched = BackgroundScheduler(daemon=True)
        sched.start()
        sched.add_job(self.gather, 'interval', seconds=120)
        atexit.register(lambda: sched.shutdown(wait=False))

    def gather(self):
        [client.run() for client in self.notifiers]

    def handleEmailNotifications(self, lastDate):
        """Places new email notifications in the Notifier's queue."""
        emails = Email.fetchUnreadEmails(self.profile, since=lastDate)
        if emails is None:
            return
        if emails:
            lastDate = Email.getMostRecentDate(emails)

        def styleEmail(e):
            subject = Email.getSubject(e, self.profile)
            if Email.isEchoEmail(e, self.profile):
                if Email.isNewEmail(e):
                    return subject.replace('[echo]', '')
                else:
                    return ""
            elif Email.isControlEmail(e, self.profile):
                self.brain.query([subject.replace('[control]', '')
                                  .strip()], None, True)
                return ""
            sender = Email.getSender(e)
            return "您有来自 %s 的新邮件 %s" % (sender, subject)
        for e in emails:
            self.q.put(styleEmail(e))

        return lastDate

    def handleRemenderNotifications(self, lastDate):
        lastDate = time.strftime('%d %b %Y %H:%M:%S')
        due_reminders = app_utils.get_due_reminders()
        for reminder in due_reminders:
            self.q.put(reminder)

        return lastDate

    def getNotification(self):
        """Returns a notification. Note that this function is consuming."""
        try:
            notif = self.q.get(block=False)
            return notif
        except Queue.Empty:
            return None

    def getAllNotifications(self):
        """
            Return a list of notifications in chronological order.
            Note that this function is consuming, so consecutive calls
            will yield different results.
        """
        notifs = []

        notif = self.getNotification()
        while notif:
            notifs.append(notif)
            notif = self.getNotification()

        return notifs
