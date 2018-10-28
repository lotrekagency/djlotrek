from django.test import TestCase, RequestFactory

from djlotrek.request_utils import get_host_url


class RequestUtilsTestCase(TestCase):

    def test_get_host_url(self):
        """
        get_host_url function retrieve request object and
        return host url when request object is not None
        """
        request_factory = RequestFactory()
        request = request_factory.get('/path')
        request.META['HTTP_HOST'] = 'localhost'
        host_url = get_host_url(request)
        self.assertEqual(host_url, 'http://localhost')

    def test_get_host_url_no_request(self):
        """
        get_host_url function retrieve request object and
        return None when request object is None
        """
        host_url = get_host_url(None)
        self.assertEqual(host_url, None)
