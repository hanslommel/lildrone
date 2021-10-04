from typing import Dict
from .ring_buffer import RingBuffer

class PublisherBase:
    """PublisherBase class.

    Messages will be shared between threads via a publisher, publishers will be 
    derived from this base class.
    """

    _buffer = None

    def __init__(self, buffer_length):
        print('Init PublisherBase')
        self._buffer = RingBuffer(buffer_length)
    
    def addOne(self, msg):
        self._buffer.append(msg)