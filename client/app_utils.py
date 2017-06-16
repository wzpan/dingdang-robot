# -*- coding: utf-8-*-
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
import logging
import os
from pytz import timezone


def sendEmail(SUBJECT, BODY, ATTACH_LIST, TO, FROM, SENDER,
              PASSWORD, SMTP_SERVER, SMTP_PORT):
    """Sends an email."""
    txt = MIMEText(BODY.encode('utf-8'), 'html', 'utf-8')
    msg = MIMEMultipart()
    msg.attach(txt)
    _logger = logging.getLogger(__name__)

    for attach in ATTACH_LIST:
        try:
            att = MIMEText(open(attach, 'rb').read(), 'base64', 'utf-8')
            filename = os.path.basename(attach)
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % filename
            msg.attach(att)
        except Exception:
            _logger.error(u'附件 %s 发送失败！' % attach)
            continue

    msg['From'] = SENDER
    msg['To'] = TO
    msg['Subject'] = SUBJECT

    try:
        session = smtplib.SMTP()
        session.connect(SMTP_SERVER, SMTP_PORT)
        session.starttls()
        session.login(FROM, PASSWORD)
        session.sendmail(SENDER, TO, msg.as_string())
        session.close()
        return True
    except Exception, e:
        _logger.error(e)
        return False


def emailUser(profile, SUBJECT="", BODY="", ATTACH_LIST=[]):
    """
    sends an email.

    Arguments:
        profile -- contains information related to the user (e.g., email
                   address)
        SUBJECT -- subject line of the email
        BODY -- body text of the email
    """
    _logger = logging.getLogger(__name__)
    # add footer
    if BODY:
        BODY = u"%s，<br><br>这是您要的内容：<br>%s<br>" % (profile['first_name'], BODY)

    recipient = profile['email']['address']
    robot_name = u'叮当'
    if profile['robot_name_cn']:
        robot_name = profile['robot_name_cn']
    recipient = robot_name + " <%s>" % recipient

    if not recipient:
        return False

    try:
        user = profile['email']['address']
        password = profile['email']['password']
        server = profile['email']['smtp_server']
        port = profile['email']['smtp_port']
        sendEmail(SUBJECT, BODY, ATTACH_LIST, user, user,
                  recipient, password, server, port)

        return True
    except Exception, e:
        _logger.error(e)
        return False


def wechatUser(profile, wxbot, SUBJECT="", BODY="",
               ATTACH_LIST=[], IMAGE_LIST=[]):
    _logger = logging.getLogger(__name__)
    if wxbot is not None and wxbot.my_account != {}:
        try:
            # send message
            user_id = wxbot.my_account['UserName']
            if BODY != '':
                wxbot.send_msg_by_uid(SUBJECT + "\n" + BODY, user_id)
            else:
                wxbot.send_msg_by_uid(SUBJECT, user_id)
            for fpath in ATTACH_LIST:
                wxbot.send_file_msg_by_uid(fpath, user_id)
            for fpath in IMAGE_LIST:
                wxbot.send_img_msg_by_uid(fpath, user_id)
            return True
            return True
        except Exception, e:
            _logger.error(e)
            return False
    return False


def sendToUser(profile, wxbot, SUBJECT="", BODY="",
               ATTACH_LIST=[], IMAGE_LIST=[]):
    send_type = 0
    if wxbot is not None and wxbot.my_account != {} \
       and ('prefers_email' not in profile or not profile['prefers_email']):
        send_type = 1
    if send_type == 0:
        return emailUser(profile, SUBJECT, BODY, ATTACH_LIST)
    else:
        return wechatUser(profile, wxbot, SUBJECT, BODY,
                          ATTACH_LIST, IMAGE_LIST)


def getTimezone(profile):
    """
    Returns the pytz timezone for a given profile.

    Arguments:
        profile -- contains information related to the user (e.g., email
                   address)
    """
    try:
        return timezone(profile['timezone'])
    except:
        return None
