# -*- coding: utf-8-*-
import Queue
import atexit
from plugins import Email
from apscheduler.schedulers.background import BackgroundScheduler
import logging


class Notifier(object):

    class NotificationClient(object):

        def __init__(self, gather, timestamp):
            self.gather = gather
            self.timestamp = timestamp

        def run(self):
            self.timestamp = self.gather(self.timestamp)

    def __init__(self, profile):
        self._logger = logging.getLogger(__name__)
        self.q = Queue.Queue()
        self.profile = profile
        self.notifiers = []

        if 'email' in profile:
            self.notifiers.append(self.NotificationClient(
                self.handleEmailNotifications, None))
        else:
            self._logger.warning('email account not set ' +
                                 'in profile, email notifier will not be used')

        sched = BackgroundScheduler(daemon=True)
        sched.start()
        sched.add_job(self.gather, 'interval', seconds=30)
        atexit.register(lambda: sched.shutdown(wait=False))

    def gather(self):
        [client.run() for client in self.notifiers]

    def handleEmailNotifications(self, lastDate):
        """Places new email notifications in the Notifier's queue."""
        emails = Email.fetchUnreadEmails(self.profile, since=lastDate)
        if emails:
            lastDate = Email.getMostRecentDate(emails)

        def styleEmail(e):
            return "您有来自 %s 的新邮件" % Email.getSender(e)

        for e in emails:
            self.q.put(styleEmail(e))

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
