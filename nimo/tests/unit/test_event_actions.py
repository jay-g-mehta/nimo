import mock
import ddt

from nimo import test
from nimo import periodic_task as nimo_periodic_task
from nimo import event_actions as nimo_event_actions
from nimo import utils as nimo_utils


@ddt.ddt
class EventActionProcessCollectorTestCase(test.TestCase):
    def tearDown(self):
        nimo_event_actions.EventActionProcessCollector.\
                             _EventActionProcessCollector__action_process_q = []
        super(EventActionProcessCollectorTestCase, self).tearDown()

    def test_add(self):
        event = mock.Mock(name='mock_event')
        action_process = mock.Mock(name='mock_process_action')
        nimo_event_actions.EventActionProcessCollector.add(
            event, action_process
        )
        self.assertEqual((event, action_process),nimo_event_actions.
                EventActionProcessCollector._EventActionProcessCollector__action_process_q[0])

    @ddt.data({'q': [(mock.Mock(name='mock_event_1'), mock.Mock(name='mock_process_action_1')),
                     (mock.Mock(name='mock_event_2'), mock.Mock(name='mock_process_action_2')),
                     ],
               'dead_process_start_index': 1,
               'dead_process_end_index': 1,
               },
              {'q': [(mock.Mock(name='mock_event_1'), mock.Mock(name='mock_process_action_1')),
                     (mock.Mock(name='mock_event_2'), mock.Mock(name='mock_process_action_2')),
                     (mock.Mock(name='mock_event_3'), mock.Mock(name='mock_process_action_3')),
                     (mock.Mock(name='mock_event_4'), mock.Mock(name='mock_process_action_4')),
                     ],
               'dead_process_start_index': 1,
               'dead_process_end_index': 2,
               },
              )
    @ddt.unpack
    def test_clean(self, q,
                   dead_process_start_index, dead_process_end_index):
        _orig_nimo_periodic_task = nimo_periodic_task
        self.patch(nimo_periodic_task, 'periodic_task', test.mask_decorator)
        reload(nimo_event_actions)

        exp_q = q[: dead_process_start_index] + q[dead_process_end_index+1:]
        dead_q = q[dead_process_start_index: dead_process_end_index+1]
        for index in range(len(q)):
            if index < dead_process_start_index or index > dead_process_end_index:
                q[index][1].is_alive.return_value = True
            else:
                q[index][1].is_alive.return_value = False
        nimo_event_actions.EventActionProcessCollector._EventActionProcessCollector__action_process_q = q

        nimo_event_actions.EventActionProcessCollector.clean()

        self.assertEqual(exp_q, nimo_event_actions.
                         EventActionProcessCollector._EventActionProcessCollector__action_process_q)

        for index in range(len(q)):
            q[index][1].is_alive.assert_called_once_with()

        for index in range(len(dead_q)):
            dead_q[index][1].is_alive.assert_called_once_with()
            dead_q[index][1].join.assert_called_once_with()

        self.patch(nimo_periodic_task, 'periodic_task', _orig_nimo_periodic_task.periodic_task)
        reload(nimo_event_actions)

@ddt.ddt
class EventActionMapperTestCase(test.TestCase):

    @ddt.data({'event_type': nimo_event_actions.libvirt.VIR_DOMAIN_EVENT_STARTED,
               'event_detail': nimo_event_actions.libvirt.VIR_DOMAIN_EVENT_STARTED_BOOTED,
               'exp_result': mock.Mock(name='mock_reconn_action_instance'),
               },
              {'event_type': 'ANY EVENT TYPE',
               'event_detail': 'ANY EVENT',
               'exp_result': None,
               },
              )
    @ddt.unpack
    @mock.patch('nimo.event_actions.ReconnEventAction')
    def test_set_get_action(self, mock_ReconnEventAction,
                            event_type, event_detail,
                            exp_result):
        mock_reconn_action_instance = exp_result
        mock_ReconnEventAction.return_value = mock_reconn_action_instance
        nimo_event_actions.EventActionMapper.set_actions()
        ret_val = nimo_event_actions.EventActionMapper.get_action(
            event_type, event_detail,
        )
        self.assertEqual(exp_result, ret_val)


class ReconnEventActionTestCase(test.TestCase):
    def setUp(self):
        super(ReconnEventActionTestCase, self).setUp()
        nimo_utils.register_default_nimo_opts()

    @mock.patch('multiprocessing.Process')
    def test_execute(self, mock_multiprocessing_process):
        mock_process = mock.Mock()
        mock_multiprocessing_process.return_value = mock_process
        reconn_action = nimo_event_actions.ReconnEventAction()
        reconn_action.execute('abolute_path_to_sample_file', 'uuid:abcd')
        mock_multiprocessing_process.assert_called_once_with(
            name='reconn_abolute_path_to_sample_file',
            target=nimo_event_actions.reconn.start_reconn,
            args=('abolute_path_to_sample_file',
                  reconn_action.reconn_config_file,
                  reconn_action.reconn_log_file,
                  reconn_action.reconn_msg_format,
                  'uuid:abcd'
                  )
        )
        self.assertEqual(True, mock_process.daemon)
        mock_process.start.assert_called_once_with()
