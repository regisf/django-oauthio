from django.conf.urls import patterns, include, url

from .views import ConnectSocialView
urlpatterns = patterns('',
    url(
        '^oauthio/connect/$',
        ConnectSocialView.as_view(),
        name="oauthio_connect"
    )
)