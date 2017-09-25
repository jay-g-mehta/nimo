import mock
import ddt

from nimo import test
from nimo import event_queue as nimo_event_queue

@ddt.ddt
class NimoEventQueueTestCase(test.TestCase):

    @ddt.data({'q_size': 10},
              {'q_size': 0},
              {'q_size': -1},
              )
    @ddt.unpack
    def test_virt_event_queue_init(self,
                                   q_size):
        q = nimo_event_queue.VirtEventQueue(q_size)
        # verify qsize
        self.assertEqual(q_size, q.q.maxsize)
        self.assertEqual(q_size, q.maxsize())


    @ddt.data({'q_size': 2,
               'item': 1,
               'block': False,
               'timeout': None,
               'item_put_count': 2,
               },
              {'q_size': 2,
               'item': {'test': 1},
               'block': False,
               'timeout': None,
               'item_put_count': 1,
               },
              )
    @ddt.unpack
    def test_virt_event_queue_put(self,
                                  q_size, item, block, timeout,
                                  item_put_count):
        q = nimo_event_queue.VirtEventQueue(q_size)
        for count in range(item_put_count):
            q.put(item, block, timeout)
        self.assertEqual(item_put_count, q.qsize())

    @ddt.data({'q_size': 2,
               'item': 1,
               'block': False,
               'timeout': None,
               },
              )
    @ddt.unpack
    @mock.patch('nimo.event_queue.native_queue.Queue.put')
    def test_virt_event_queue_put_overflow(self, mock_native_queue_put,
                                           q_size, item, block, timeout):
        q = nimo_event_queue.VirtEventQueue(q_size)
        mock_native_queue_put.side_effect = nimo_event_queue.native_queue.Full
        q.put(item, block, timeout)

    @ddt.data({'q_size': 2,
               'item': 1,
               'block': False,
               'timeout': None,
               },
              {'q_size': 2,
               'item': {'test': 1},
               'block': False,
               'timeout': None,
               },
              )
    @ddt.unpack
    @mock.patch('nimo.event_queue.native_queue.Queue.get')
    def test_virt_event_queue_get(self, mock_native_queue_get,
                                  q_size, item, block, timeout):
        q = nimo_event_queue.VirtEventQueue(q_size)
        mock_native_queue_get.return_value = item
        ret_val = q.get(block, timeout)
        self.assertEqual(item, ret_val)

    @ddt.data({'q_size': 2,
               'item': None,
               'block': False,
               'timeout': None,
               },
              )
    @ddt.unpack
    @mock.patch('nimo.event_queue.native_queue.Queue.get')
    def test_virt_event_queue_get_underflow(self, mock_native_queue_get,
                                            q_size, item, block, timeout):
        q = nimo_event_queue.VirtEventQueue(q_size)
        mock_native_queue_get.side_effect = nimo_event_queue.native_queue.Empty
        ret_val = q.get(block, timeout)
        self.assertEqual(item, ret_val)
