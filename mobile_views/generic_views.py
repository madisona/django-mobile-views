
from django.views import generic

from mobile_views import utilities

__all__ = (
    'MobileTemplateView', 'MobileDetailView', 'MobileFormView',
    'MobileCreateView', 'MobileRedirectView',
)

class MobileMixin(object):
    """
    MobileMixin is a supplement to django's generic views.

    The mobile mixin uses the user agent to match a regular expression
    that is know to indicate a mobile device.

    If the device is mobile and the user doesn't have a 'no_mobile'
    cookie set, the Mixin will try to render the mobile template if
    it exists, falling back to the regular template if not.

    """
    template_name = None
    mobile_template_name = None

    def use_mobile(self):
        return utilities.use_mobile(self.request)

    def set_mobile_cookie(self, response):
        response.set_cookie('no_mobile', True)

    def delete_mobile_cookie(self, response):
        response.delete_cookie('no_mobile')

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.use_mobile():
            return self.get_mobile_template_name()
        else:
            return self.get_default_template_name()

    def get_default_template_name(self):
        if self.template_name is None:
            return []
        return [self.template_name]

    def get_mobile_template_name(self):
        if self.mobile_template_name is None:
            return self.get_default_template_name()
        return [self.mobile_template_name]


# The views below just piggyback on django's generic views
# adding the mobile mixin...

class MobileTemplateView(MobileMixin, generic.TemplateView):
    pass

class MobileDetailView(MobileMixin, generic.DetailView):
    pass

class MobileFormView(MobileMixin, generic.FormView):
    pass

class MobileCreateView(MobileMixin, generic.CreateView):
    pass

class MobileRedirectView(MobileMixin, generic.RedirectView):
    permanent = False