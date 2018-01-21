# -*- coding: utf-8-*-
"""
    The Mic class handles all interactions with the microphone and speaker.
"""
from __future__ import absolute_import
import ctypes
import logging
import tempfile
import wave
import audioop
import time
import pyaudio
from . import dingdangpath
from . import mute_alsa
from .app_utils import wechatUser


class Mic:
    speechRec = None
    speechRec_persona = None

    def __init__(self, profile, speaker, passive_stt_engine,
                 active_stt_engine):
        """
        Initiates the pocketsphinx instance.

        Arguments:
        profile -- config profile
        speaker -- handles platform-independent audio output
        passive_stt_engine -- performs STT while Dingdang is in passive listen
                              mode
        acive_stt_engine -- performs STT while Dingdang is in active listen
                            mode
        """
        self.profile = profile
        self.robot_name = u'叮当'
        if 'robot_name_cn' in profile:
            self.robot_name = profile['robot_name_cn']
        self._logger = logging.getLogger(__name__)
        self.speaker = speaker
        self.wxbot = None
        self.passive_stt_engine = passive_stt_engine
        self.active_stt_engine = active_stt_engine
        self.dingdangpath = dingdangpath
        self._logger.info("Initializing PyAudio. ALSA/Jack error messages " +
                          "that pop up during this process are normal and " +
                          "can usually be safely ignored.")
        try:
            asound = ctypes.cdll.LoadLibrary('libasound.so.2')
            asound.snd_lib_error_set_handler(mute_alsa.c_error_handler)
        except OSError:
            pass
        self._audio = pyaudio.PyAudio()
        self._logger.info("Initialization of PyAudio completed.")
        self.stop_passive = False
        self.skip_passive = False
        self.chatting_mode = False

    def __del__(self):
        self._audio.terminate()

    def getScore(self, data):
        rms = audioop.rms(data, 2)
        score = rms / 3
        return score

    def fetchThreshold(self):

        # TODO: Consolidate variables from the next three functions
        THRESHOLD_MULTIPLIER = 2.5
        RATE = 16000
        CHUNK = 1024

        # number of seconds to allow to establish threshold
        THRESHOLD_TIME = 1

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        # stores the audio data
        frames = []

        # stores the lastN score values
        lastN = [i for i in range(20)]

        # calculate the long run average, and thereby the proper threshold
        for i in range(0, RATE / CHUNK * THRESHOLD_TIME):
            try:
                data = stream.read(CHUNK)
                frames.append(data)

                # save this data point as a score
                lastN.pop(0)
                lastN.append(self.getScore(data))
                average = sum(lastN) / len(lastN)

            except Exception as e:
                self._logger.debug(e)
                continue

        try:
            stream.stop_stream()
            stream.close()
        except Exception as e:
            self._logger.debug(e)
            pass

        # this will be the benchmark to cause a disturbance over!
        THRESHOLD = average * THRESHOLD_MULTIPLIER

        return THRESHOLD

    def stopPassiveListen(self):
        """
        Stop passive listening
        """
        self.stop_passive = True

    def passiveListen(self, PERSONA):
        """
        Listens for PERSONA in everyday sound. Times out after LISTEN_TIME, so
        needs to be restarted.
        """

        THRESHOLD_MULTIPLIER = 2.5
        RATE = 16000
        CHUNK = 1024

        # number of seconds to allow to establish threshold
        THRESHOLD_TIME = 1

        # number of seconds to listen before forcing restart
        LISTEN_TIME = 10

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        # stores the audio data
        frames = []

        # stores the lastN score values
        lastN = [i for i in range(30)]

        didDetect = False

        # calculate the long run average, and thereby the proper threshold
        for i in range(0, RATE / CHUNK * THRESHOLD_TIME):

            try:
                if self.stop_passive:
                    self._logger.debug('stop passive')
                    break

                data = stream.read(CHUNK)

                # save this data point as a score
                lastN.pop(0)
                lastN.append(self.getScore(data))
                average = sum(lastN) / len(lastN)

                # this will be the benchmark to cause a disturbance over!
                THRESHOLD = average * THRESHOLD_MULTIPLIER

                # flag raised when sound disturbance detected
                didDetect = False
            except Exception as e:
                self._logger.debug(e)
                pass

        # start passively listening for disturbance above threshold
        for i in range(0, RATE / CHUNK * LISTEN_TIME):

            try:
                if self.stop_passive:
                    self._logger.debug('stop passive')
                    break

                data = stream.read(CHUNK)
                frames.append(data)
                score = self.getScore(data)

                if score > THRESHOLD:
                    didDetect = True
                    break
            except Exception as e:
                self._logger.debug(e)
                continue

        # no use continuing if no flag raised
        if not didDetect:
            self._logger.debug("没接收到唤醒指令")
            try:
                # self.stop_passive = False
                stream.stop_stream()
                stream.close()
            except Exception as e:
                self._logger.debug(e)
                pass
            return (None, None)

        # cutoff any recording before this disturbance was detected
        frames = frames[-20:]

        # otherwise, let's keep recording for few seconds and save the file
        DELAY_MULTIPLIER = 1
        for i in range(0, RATE / CHUNK * DELAY_MULTIPLIER):

            try:
                if self.stop_passive:
                    break
                data = stream.read(CHUNK)
                frames.append(data)
            except Exception as e:
                self._logger.debug(e)
                continue

        # save the audio data
        try:
            # self.stop_passive = False
            stream.stop_stream()
            stream.close()
        except Exception as e:
            self._logger.debug(e)
            pass

        transcribed = self.passive_stt_engine.transcribe_keyword(
            ''.join(frames))

        if transcribed is not None and \
           any(PERSONA in phrase for phrase in transcribed):
            return (THRESHOLD, PERSONA)

        return (False, transcribed)

    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        """
            Records until a second of silence or times out after 12 seconds

            Returns the first matching string or None
        """

        options = self.activeListenToAllOptions(THRESHOLD, LISTEN, MUSIC)
        if options:
            return options[0]

    def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True,
                                 MUSIC=False):
        """
            Records until a second of silence or times out after 12 seconds

            Returns a list of the matching options or None
        """

        RATE = 16000
        CHUNK = 1024
        LISTEN_TIME = 12

        # check if no threshold provided
        if THRESHOLD is None:
            THRESHOLD = self.fetchThreshold()

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        self.speaker.play(dingdangpath.data('audio', 'beep_hi.wav'))

        frames = []
        # increasing the range # results in longer pause after command
        # generation
        lastN = [THRESHOLD * 1.2 for i in range(40)]

        for i in range(0, RATE / CHUNK * LISTEN_TIME):
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                score = self.getScore(data)

                lastN.pop(0)
                lastN.append(score)

                average = sum(lastN) / float(len(lastN))

                # TODO: 0.8 should not be a MAGIC NUMBER!
                if average < THRESHOLD * 0.8:
                    break
            except Exception as e:
                self._logger.error(e)
                continue

        self.speaker.play(dingdangpath.data('audio', 'beep_lo.wav'))

        # save the audio data
        try:
            stream.stop_stream()
            stream.close()
        except Exception as e:
            self._logger.debug(e)
            pass

        with tempfile.SpooledTemporaryFile(mode='w+b') as f:
            wav_fp = wave.open(f, 'wb')
            wav_fp.setnchannels(1)
            wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            wav_fp.setframerate(RATE)
            wav_fp.writeframes(''.join(frames))
            wav_fp.close()
            f.seek(0)
            frames = []
            return self.active_stt_engine.transcribe(f)

    def say(self, phrase,
            OPTIONS=" -vdefault+m3 -p 40 -s 160 --stdout > say.wav",
            cache=False):
        self._logger.info(u"机器人说：%s" % phrase)
        self.stop_passive = True
        if self.wxbot is not None:
            wechatUser(self.profile, self.wxbot, "%s: %s" %
                       (self.robot_name, phrase), "")
        # incase calling say() method which
        # have not implement cache feature yet.
        # the count of args should be 3.
        if self.speaker.say.__code__.co_argcount > 2:
            self.speaker.say(phrase, cache)
        else:
            self.speaker.say(phrase)
        time.sleep(1)  # 避免叮当说话时误唤醒
        self.stop_passive = False

    def play(self, src):
        # play a voice
        self.speaker.play(src)
