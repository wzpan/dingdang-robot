#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import os
from pydub import AudioSegment


def mp3_to_wav(mp3_file):
    target = mp3_file.replace(".mp3", ".wav")
    if os.path.exists(mp3_file):
        voice = AudioSegment.from_mp3(mp3_file)
        voice.export(target, format="wav")
        return target
    else:
        print(u"文件错误")
