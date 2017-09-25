import mock
import ddt

from nimo import test
from nimo import periodic_task as nimo_periodic_task


@ddt.ddt
class PeriodicTaskTestCase(test.TestCase):

    @mock.patch('time.sleep')
    @mock.patch('threading.Thread')
    def test_task(self,
                  mock_threadingThread,
                  mock_time_sleep):

        exp_args = (1, 2)
        exp_kwargs = {'test': 'test'}

        @nimo_periodic_task.periodic_task(10)
        def func_under_periodic_task_test(*args, **kwargs):
            self.assertEqual(exp_args, args)
            self.assertEqual(exp_kwargs, kwargs)
            raise KeyboardInterrupt

        mock_thread_obj = mock.Mock()
        mock_threadingThread.return_value = mock_thread_obj

        func_under_periodic_task_test(*exp_args, **exp_kwargs)

        mock_threadingThread.assert_called_once()
        self.assertEqual(True, mock_thread_obj.daemon)
        mock_thread_obj.start.assert_called_once()

        mock_thread_args, mock_thread_kargs = mock_threadingThread.call_args
        self.assertRaises(KeyboardInterrupt,
                          mock_thread_kargs['target'],
                          *mock_thread_kargs['args'], **mock_thread_kargs['kwargs']
                          )
