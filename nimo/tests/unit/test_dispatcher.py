import ddt
import mock

from nimo import test
from nimo import dispatcher as nimo_dispatcher


@ddt.ddt
class NimoDispatcherTestCase(test.TestCase):

    @ddt.data({'thread_type': 'greenthread'},
              {'thread_type': 'nativethread'},
              )
    @ddt.unpack
    @mock.patch('nimo.dispatcher.Dispatcher._green_thread_dispatcher')
    @mock.patch('nimo.dispatcher.Dispatcher._native_thread_dispatcher')
    def test_create_dispatcher(self,
                               mock_nimo_native_dipatcher,
                               mock_nimo_gt_dispatcher,
                               thread_type):
        dispatch_target_f = mock.Mock()
        ret_val = nimo_dispatcher.Dispatcher.create(thread_type,
                                                    dispatch_target_f,
                                                    )
        if thread_type == 'greenthread':
            mock_nimo_gt_dispatcher.assert_called_once_with(
                dispatch_target_f
            )
        elif thread_type == 'nativethread':
            mock_nimo_native_dipatcher.assert_called_once_with(
                dispatch_target_f
            )
        self.assertEqual(nimo_dispatcher.Dispatcher, ret_val.__class__)
        self.assertEqual(thread_type, ret_val.t_type)
