# -*- coding: utf-8-*-
import logging
import pkgutil
import dingdangpath

class Brain(object):

    def __init__(self, mic, profile):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of modules. Note that the order of brain.modules
        matters, as the Brain will cease execution on the first module
        that accepts a given input.

        Arguments:
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        """

        self.mic = mic
        self.profile = profile
        self.modules = self.get_modules()
        self._logger = logging.getLogger(__name__)
        self.handling = False

    @classmethod
    def get_modules(cls):
        """
        Dynamically loads all the modules in the modules folder and sorts
        them by the PRIORITY key. If no PRIORITY is defined for a given
        module, a priority of 0 is assumed.
        """

        logger = logging.getLogger(__name__)
        locations = [dingdangpath.PLUGIN_PATH, dingdangpath.CONTRIB_PATH]
        logger.debug("Looking for modules in: %s",
                     ', '.join(["'%s'" % location for location in locations]))
        modules = []
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except:
                logger.warning("Skipped module '%s' due to an error.", name,
                               exc_info=True)
            else:
                if hasattr(mod, 'WORDS'):
                    logger.debug("Found module '%s' with words: %r", name,
                                 mod.WORDS)
                    modules.append(mod)
                else:
                    logger.warning("Skipped module '%s' because it misses " +
                                   "the WORDS constant.", name)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                     else 0, reverse=True)
        return modules

    def query(self, texts, wxbot=None):
        """
        Passes user input to the appropriate module, testing it against
        each candidate module's isValid function.

        Arguments:
        text -- user input, typically speech, to be parsed by a module
        send_wechat -- also send the respondsed result to wechat
        """
        for module in self.modules:
            for text in texts:
                if module.isValid(text):
                    self._logger.debug("'%s' is a valid phrase for module " +
                                       "'%s'", text, module.__name__)
                    try:
                        handling = True
                        module.handle(text, self.mic, self.profile, wxbot)
                        handling = False
                    except Exception:
                        self._logger.error('Failed to execute module',
                                           exc_info=True)
                        reply = u"抱歉，我的大脑出故障了，晚点再试试吧"
                        self.mic.say(reply)
                    else:
                        self._logger.debug("Handling of phrase '%s' by " +
                                           "module '%s' completed", text,
                                           module.__name__)
                    finally:
                        return
        self._logger.debug("No module was able to handle any of these " +
                           "phrases: %r", texts)
        
