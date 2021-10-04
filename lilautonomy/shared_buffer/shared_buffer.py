
import threading
import time as timelib
from . import message_base
from . import publisher_base


class SharedBuffer:
    """SharedBuffer class.

    Singleton class for sharing data between threads.  All publishers will be managed by the
    SharedBuffer class, and threads will access publishers through it.
    """

    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if SharedBuffer.__instance == None:
            SharedBuffer()
        return SharedBuffer.__instance
    def __init__(self):
        """ Virtually private constructor. """
        print('Init SharedBuffer')
        if SharedBuffer.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SharedBuffer.__instance = self
