#!/usr/bin/env python2
# -*- coding: utf-8-*-
from nose.tools import *
import mock
from client import brain, test_mic


DEFAULT_PROFILE = {
    'prefers_email': False,
    'timezone': 'HKT'
}


class TestBrain():

    @staticmethod
    def _emptyBrain():
        mic = test_mic.Mic([])
        profile = DEFAULT_PROFILE
        return brain.Brain(mic, profile)

    def testSortByPriority(self):
        """Does Brain sort plugins by priority?"""
        my_brain = TestBrain._emptyBrain()
        priorities = filter(lambda m: hasattr(m, 'PRIORITY'), my_brain.plugins)
        target = sorted(priorities, key=lambda m: m.PRIORITY, reverse=True)
        assert target == priorities

    def testPriority(self):
        """Does Brain correctly send query to higher-priority plugin?"""
        my_brain = TestBrain._emptyBrain()
        echo_plugin = 'Echo'
        hn = filter(lambda m: m.__name__ == echo_plugin, my_brain.plugins)[0]

        with mock.patch.object(hn, 'handle') as mocked_handle:
            my_brain.query(["echo 你好吗"])
            assert mocked_handle.called
