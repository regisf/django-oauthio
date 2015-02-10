
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def oauthio_install_javascript():
    """
    Get the javascript file for Oauth.io
    :return: A script tag
    """
    tpl = '<script type="text/javascript" src="{0}"></script>'
#    if getattr(settings, "DEBUG", False):
    return '{0}\n{1}'.format(tpl.format(
        getattr(
            settings,
            "OAUTHIO_JAVASCRIPT_SRC",
            # Serve oauth.io GitHub file with the correct mime type
             "https://cdn.rawgit.com/oauth-io/oauth-js/master/dist/oauth.js"
        )
    ), tpl.format(settings.STATIC_URL + 'oauthio.js'))
#    else:
#        return tpl.format(settings.STATIC_URL + "oauth-io-full.min.js")

