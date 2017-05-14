# -*- coding: utf-8-*-
import imaplib
import email
import re
from dateutil import parser

WORDS = ["EMAIL", "INBOX"]


def getSender(email):
    """
        Returns the best-guess sender of an email.

        Arguments:
        email -- the email whose sender is desired

        Returns:
        Sender of the email.
    """
    sender = email['From']
    start_pos = sender.find('<')
    end_pos = sender.find('>')
    if start_pos > -1 and end_pos > -1:
        sender = sender[start_pos+1:end_pos]
    return sender


def getDate(email):
    return parser.parse(email.get('date'))


def getMostRecentDate(emails):
    """
        Returns the most recent date of any email in the list provided.

        Arguments:
        emails -- a list of emails to check

        Returns:
        Date of the most recent email.
    """
    dates = [getDate(e) for e in emails]
    dates.sort(reverse=True)
    if dates:
        return dates[0]
    return None


def fetchUnreadEmails(profile, since=None, markRead=False, limit=None):
    """
        Fetches a list of unread email objects from a user's email inbox.

        Arguments:
        profile -- contains information related to the user (e.g., email
                   address)
        since -- if provided, no emails before this date will be returned
        markRead -- if True, marks all returned emails as read in target inbox

        Returns:
        A list of unread email objects.
    """

    conn = imaplib.IMAP4(profile['email']['imap_server'], profile['email']['imap_port'])
    conn.debug = 0
    conn.login(profile['email']['address'], profile['email']['password'])
    conn.select(readonly=(not markRead))

    msgs = []
    (retcode, messages) = conn.search(None, '(UNSEEN)')

    if retcode == 'OK' and messages != ['']:
        numUnread = len(messages[0].split(' '))
        if limit and numUnread > limit:
            return numUnread

        for num in messages[0].split(' '):
            # parse email RFC822 format
            ret, data = conn.fetch(num, '(RFC822)')
            msg = email.message_from_string(data[0][1])

            if not since or getDate(msg) > since:
                msgs.append(msg)
    conn.close()
    conn.logout()

    return msgs


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, with a summary of
        the user's email inbox, reporting on the number of unread emails
        in the inbox, as well as their senders.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., email
                   address)
    """
    try:
        msgs = fetchUnreadEmails(profile, limit=5)

        if isinstance(msgs, int):
            response = "您有 %d 封未读邮件" % msgs            
            mic.say(response)
            return

        senders = [getSender(e) for e in msgs]
    except imaplib.IMAP4.error:
        mic.say(
            u"抱歉，您的邮箱账户验证失败了")
        return

    if not senders:
        mic.say(u"您没有未读邮件，真棒！")
    elif len(senders) == 1:
        mic.say(u"您有来自 " + senders[0] + " 的未读邮件")
    else:
        response = u"您有 %d 封未读邮件" % len(
            senders)
        unique_senders = list(set(senders))
        if len(unique_senders) > 1:
            unique_senders[-1] = ', ' + unique_senders[-1]
            response += "。这些邮件的发件人包括："
            response += ' 和 '.join(senders)
        else:
            response += "，邮件都来自 " + unique_senders[0]
        mic.say(response)


def isValid(text):
    """
        Returns True if the input is related to email.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in [u'邮箱', u'邮件'])
