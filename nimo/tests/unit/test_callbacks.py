import mock

from nimo import test
from nimo import callbacks as nimo_callbacks


class NimoCallbacksTestCase(test.TestCase):

    @mock.patch.object(nimo_callbacks, 'event_queued_notify_send')
    @mock.patch.object(nimo_callbacks, 'event_q')
    @mock.patch('nimo.event_queue.VirtLifeCycleEvent')
    def test_virt_event_callback(self,
                                 mock_nimo_virtlifecycleevent,
                                 mock_nimo_callbacks_event_q,
                                 mock_nimo_callbacks_event_queued_notify_send):
        conn = mock.Mock(name='mock_virt_conn')
        dom = mock.Mock(name='mock_virt_domain')
        event = mock.Mock(name='mock_virt_event')
        detail = mock.Mock(name='mock_virt_event_detail')
        opaque_userdata = mock.Mock(name='mock_virt_opaque_userdata')

        mock_nimo_virt_event = mock.Mock(name='nimo_virt_life_cycle_event')
        mock_nimo_virtlifecycleevent.return_value = mock_nimo_virt_event

        nimo_callbacks.domain_lifecycle_event_callback(conn, dom,
                                                       event, detail,
                                                       opaque_userdata)
        mock_nimo_virtlifecycleevent.assert_called_once_with(conn, dom,
                                                             event, detail,
                                                             opaque_userdata)

        mock_nimo_callbacks_event_q.put.assert_called_once_with(
            mock_nimo_virt_event
        )
        mock_nimo_callbacks_event_queued_notify_send.write.assert_called_once()
        mock_nimo_callbacks_event_queued_notify_send.flush.\
            assert_called_once_with()
