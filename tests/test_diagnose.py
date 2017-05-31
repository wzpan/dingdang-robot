#!/usr/bin/env python2
# -*- coding: utf-8-*-
from nose.tools import *
from client import diagnose


def testPythonImportCheck():
    # This a python stdlib module that definitely exists
    assert diagnose.check_python_import("os")
    # I sincerly hope nobody will ever create a package with that name
    assert not diagnose.check_python_import("nonexistant_package")
