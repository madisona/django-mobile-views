
from django.conf.urls.defaults import patterns, url

from mobile_views import views

urlpatterns = patterns('',
    url(r'full-site/$', views.FullSiteView.as_view(), name="full_site"),
)