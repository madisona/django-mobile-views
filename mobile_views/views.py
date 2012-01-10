__author__ = 'amadison'

from mobile_views.generic_views import MobileRedirectView


__all__ = ('FullSiteView', )

class FullSiteView(MobileRedirectView):
    """
    this view will set a 'no_mobile' cookie and redirect to whatever
    the follow url is. The cookie will remain for the session of the
    browser and prevent any further re-directing to a mobile template.
    """

    def get_redirect_url(self, **kwargs):
        return self.request.GET.get('follow', '/')

    def get(self, request, *args, **kwargs):
        response = super(FullSiteView, self).get(request, *args, **kwargs)
        self.set_mobile_cookie(response)
        return response
