
import mock

from django import test
from django.http import HttpResponse, HttpRequest

from mobile_views import views, utilities, generic_views

class MobileMixinTests(test.TestCase):

    def setUp(self):
        self.request = mock.Mock(spec=HttpRequest)
        self.request.META = {}
        self.mixin = generic_views.MobileMixin()
        self.mixin.request = self.request

    def test_sets_no_mobile_cookie(self):
        response = mock.Mock(spec=HttpResponse)
        self.mixin.set_mobile_cookie(response)
        self.assertEqual((('no_mobile', True), {}), response.set_cookie.call_args)

    def test_deletes_no_mobile_cookie(self):
        response = mock.Mock(spec=HttpResponse)
        self.mixin.delete_mobile_cookie(response)
        self.assertEqual((('no_mobile',), {}), response.delete_cookie.call_args)

    @mock.patch('mobile_views.utilities.use_mobile', mock.Mock(return_value=True))
    def test_return_true_when_utilities_function_uses_mobile(self):
        self.assertEqual(True, self.mixin.use_mobile())

    @mock.patch('mobile_views.utilities.use_mobile', mock.Mock(return_value=False))
    def test_return_true_when_utilities_function_uses_mobile(self):
        self.assertEqual(False, self.mixin.use_mobile())

    @mock.patch('mobile_views.generic_views.MobileMixin.use_mobile', mock.Mock(return_value=True))
    def test_returns_mobile_template_name_when_use_mobile(self):
        self.mixin.mobile_template_name = mock.sentinel.mobile_template_name
        self.assertEqual([self.mixin.mobile_template_name], self.mixin.get_template_names())

    @mock.patch('mobile_views.generic_views.MobileMixin.use_mobile', mock.Mock(return_value=False))
    def test_returns_template_name_when_not_use_mobile(self):
        self.mixin.template_name = mock.sentinel.template_name
        self.assertEqual([self.mixin.template_name], self.mixin.get_template_names())

    @mock.patch('mobile_views.generic_views.MobileMixin.use_mobile', mock.Mock(return_value=False))
    def test_returns_empty_list_when_not_use_mobile_and_template_name_not_defined(self):
        self.assertEqual([], self.mixin.get_template_names())

class MobileUtilitiesTests(test.TestCase):

    def test_returns_true_when_user_agent_matches_android(self):
        request = mock.Mock(spec=HttpRequest)
        request.META = {'HTTP_USER_AGENT': 'android'}
        self.assertTrue(utilities.is_mobile(request))

    def test_returns_true_when_user_agent_matches_iphone(self):
        request = mock.Mock(spec=HttpRequest)
        request.META = {'HTTP_USER_AGENT': 'iphone'}
        self.assertTrue(utilities.is_mobile(request))

    def test_returns_false_when_user_agent_does_not_match_lists(self):
        request = mock.Mock(spec=HttpRequest)
        request.META = {'HTTP_USER_AGENT': 'chrome'}
        self.assertFalse(utilities.is_mobile(request))

    def test_returns_true_when_user_has_no_mobile_cookie(self):
        request = mock.Mock(spec=HttpRequest)
        request.COOKIES = {'no_mobile': 'True'}
        self.assertTrue(utilities.user_declined_mobile(request))

    def test_returns_false_when_user_does_not_have_no_mobile_cookie(self):
        request = mock.Mock(spec=HttpRequest)
        request.COOKIES = {}
        self.assertFalse(utilities.user_declined_mobile(request))

    @mock.patch('mobile_views.utilities.is_mobile', mock.Mock(return_value=True))
    @mock.patch('mobile_views.utilities.user_declined_mobile', mock.Mock(return_value=False))
    def test_returns_true_when_is_mobile_and_not_user_declined_mobile(self):
        self.assertEqual(True, utilities.use_mobile(mock.Mock()))

    @mock.patch('mobile_views.utilities.is_mobile', mock.Mock(return_value=False))
    @mock.patch('mobile_views.utilities.user_declined_mobile', mock.Mock(return_value=False))
    def test_returns_false_when_not_is_mobile(self):
        self.assertEqual(False, utilities.use_mobile(mock.Mock()))

    @mock.patch('mobile_views.utilities.is_mobile', mock.Mock(return_value=True))
    @mock.patch('mobile_views.utilities.user_declined_mobile', mock.Mock(return_value=True))
    def test_returns_false_when_is_mobile_and_user_declined_mobile(self):
        self.assertEqual(False, utilities.use_mobile(mock.Mock()))

class FullSiteViewTests(test.TestCase):

    def setUp(self):
        self.view = views.FullSiteView()

    def test_returns_follow_parameter(self):
        self.view.request = mock.Mock()
        self.view.request.GET = {'follow': mock.sentinel.follow}
        self.assertEqual(mock.sentinel.follow, self.view.get_redirect_url())

    def test_returns_root_url_when_no_follow_parameter(self):
        self.view.request = mock.Mock()
        self.view.request.GET = {}
        self.assertEqual('/', self.view.get_redirect_url())

    @mock.patch('mobile_views.views.FullSiteView.set_mobile_cookie')
    @mock.patch('mobile_views.views.MobileRedirectView.get')
    def test_sets_mobile_cookie_on_get_request(self, redirect_get, set_mobile_cookie):
        response = mock.Mock(spec=HttpResponse)
        redirect_get.return_value = response
        views.FullSiteView().get(mock.Mock())
        self.assertTrue(((response,), {}), set_mobile_cookie.call_args)
