
import threading

from django.test import TestCase, override_settings

from mock import MagicMock, Mock, patch, call

from amp_tools import get_amp_detect
from amp_tools.middleware import AMPDetectionMiddleware

def _reset():
    '''
    Reset the thread local.
    '''
    import amp_tools
    del amp_tools._local
    amp_tools._local = threading.local()


class BaseTestCase(TestCase):
    def setUp(self):
        _reset()

    def tearDown(self):
        _reset()


class DetectAMPMiddlewareTests(BaseTestCase):

    def test_default_page(self):
        request = Mock()
        request.META = MagicMock()
        request.GET = {}
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        # default flavour is set
        self.assertEqual(get_amp_detect(), '')

    @patch('amp_tools.middleware.set_amp_detect')
    def test_set_amp_detect_through_get_parameter(self, set_amp_detect):
        request = Mock()
        request.META = MagicMock()
        request.GET = {'amp-content': 'amp'}
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(set_amp_detect.call_args, call(is_amp_detect=True, request=request))

    @patch('amp_tools.middleware.set_amp_detect')
    @override_settings(AMP_TOOLS_ACTIVE_URLS=['^/$'])
    def test_set_amp_not_set_url_not_allowed(self, set_amp_detect):
        request = Mock()
        request.META = MagicMock()
        request.GET = {'amp-content': 'amp'}
        request.path_info = '/'
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(set_amp_detect.call_args, call(is_amp_detect=True, request=request))

    @patch('amp_tools.middleware.set_amp_detect')
    @override_settings(AMP_TOOLS_ACTIVE_URLS=['^/$'])
    def test_set_amp_not_set_url_not_allowed(self, set_amp_detect):
        request = Mock()
        request.META = MagicMock()
        request.GET = {'amp-content': 'amp'}
        request.path_info = '/not-amp-url/'
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(0, len(set_amp_detect.call_args_list))

