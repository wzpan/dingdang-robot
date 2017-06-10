#!/usr/bin/env python2
# -*- coding: utf-8-*-
from nose.tools import *
from client import test_mic, diagnose, dingdangpath
from client.plugins import Time, Echo, Email, SendQR

DEFAULT_PROFILE = {
    'prefers_email': False,
    'timezone': 'HKT',
    'wechat': False
}


class TestPlugins():

    def setUp(self):
        self.profile = DEFAULT_PROFILE
        self.send = False

    def runConversation(self, query, inputs, module):
        """Generic method for spoofing conversation.

        Arguments:
        query -- The initial input to the server.
        inputs -- Additional input, if conversation is extended.

        Returns:
        The server's responses, in a list.
        """
        assert module.isValid(query)
        mic = test_mic.Mic(inputs)
        module.handle(query, mic, self.profile)
        return mic.outputs

    def testEcho(self):
        query = u"echo 你好吗"
        inputs = []
        outputs = self.runConversation(query, inputs, Echo)
        assert outputs[0].strip() == u'你好吗'

    def testTime(self):
        query = u"现在几点"
        inputs = []
        outputs = self.runConversation(query, inputs, Time)
        assert u'现在时间是' in outputs[0]

    def testEmail(self):
        if 'email' not in self.profile or 'enable' not in self.profile['email']:
            return
        
        query = u"我有多少邮件"
        inputs = []
        self.runConversation(query, inputs, Gmail)

    def testSendQR(self):
        if 'wechat' not in self.profile or not self.profile['wechat']:
            return
        
        query = u"发送微信二维码"
        inputs = []
        self.runConversation(query, inputs, SendQR)

        
