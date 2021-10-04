from . import ring_buffer

class PublisherBase:
    """PublisherBase class.

    Messages will be shared between threads via a publisher, publishers will be 
    derived from this base class.
    """

    _buffer = None

    def __init__(self, buffer_length):
        print('Init PublisherBase')
        _buffer = ring_buffer.RingBuffer(buffer_length)