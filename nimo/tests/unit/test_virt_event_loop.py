import mock

from nimo import test
from nimo import virt_api as nimo_virt_api


class NimoVirtEventLoopTestCase(test.TestCase):

    @mock.patch('nimo.virt_api.native_threading')
    @mock.patch('nimo.virt_api.libvirt')
    def test_startVirEventLoop(self,
                               mock_libvirt,
                               mock_nimo_native_threading):
        mock_event_loop_thread = mock.Mock(name='mock_event_loop_thread')
        mock_nimo_native_threading.Thread.return_value = mock_event_loop_thread
        ret_val = nimo_virt_api.startVirEventLoop()
        mock_libvirt.assert_has_calls(
            [mock.call.virEventRegisterDefaultImpl(), ]
        )
        mock_libvirt.virEventRegisterDefaultImpl.assert_called_once_with()
        mock_nimo_native_threading.Thread.assert_called_once_with(
            target=nimo_virt_api._runVirDefaultEventLoop,
            name="libvirtEventLoop"
        )
        mock_event_loop_thread.setDaemon.assert_called_once_with(True)
        mock_event_loop_thread.start.assert_called_once_with()
        self.assertEqual(mock_event_loop_thread, ret_val)

    @mock.patch('nimo.virt_api.libvirt.virEventRunDefaultImpl')
    def test_run_virt_default_event_loop(self,
                                         mock_virEventRunDefaultImpl):
        # Verifying infinite loop in _runVirDefaultEventLoop, by looping
        # virEventRunDefaultImpl() for 2 times and then raise StopIteration
        # to break the while loop
        mock_virEventRunDefaultImpl.side_effect = [True, True, StopIteration]
        self.assertRaises(StopIteration,
                          nimo_virt_api._runVirDefaultEventLoop, )
        mock_virEventRunDefaultImpl.assert_called_with()
        self.assertEqual(mock_virEventRunDefaultImpl.call_count, 3)
