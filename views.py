# -*- coding: UTF-8 -*-
# OAuth.io service for Django
# (c) Régis FLORET 2015 and later
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Using oauth.io services with Django.
"""
from django.utils import timezone
import json

import httplib2
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from .signals import oauthio_user_signin, user_registration_problem
from .models import OAuthioUser

__author__ = 'Regis FLORET'
__version__ = '1.0'
__license__ = 'MIT'


def convert_request_to_json(request):
    """
    Convert a request to a json object. The request could be in the query
    http://somewhe.re/?json=[JSON.stringify object] or in the body.

    :param request: The web request
    :rtype request: HttpRequest
    :return The data or an empty dictionary
    :rtype dict
    """
    data = request.POST.get('json') if request.method == 'POST' else request.GET.get('json', None)
    data_json = None

    if data:
        data_json = json.loads(data)

    elif len(request.META['QUERY_STRING'].strip()) > 0:
        data_json = json.loads(request.META['QUERY_STRING'].replace("%22", '"'))

    elif len(request.body.strip()) > 0:
        data_json = json.loads(request.body)

    return data_json or {}


#
# All the known providers control URL
# TODO: In a separate file due to the huge oauth.io provider collection
#
PROVIDERS = {
    'facebook': 'https://graph.facebook.com/me?fields=id&access_token={}',
    'google': 'https://www.googleapis.com/plus/v1/people/me?access_token={}',
    'linkedin': 'https://api.linkedin.com/v1/people/~?oauth2_access_token={}&format=json',
    'twitter': 'https://api.twitter.com/oauth/access_token',
    'yahoo': 'http://social.yahooapis.com/v1/user/{}/profile?format=json',
    # 'live': ''
}


class ConnectSocialView(View):
    """
    Create and Connect an user comming from social network

    Implements only POST method.
    """

    def post(self, request):
        """
        Process to the connection.

        If the user exists, just login else create h{im,er}

        :param request: The django request object
        :type request: HttpRequest
        :return: A dictionnary containing at least the key success which is True on success
        :rtype: dict
        """
        data = convert_request_to_json(request)

        # access_token, email and username are required
        # So if one of these aren't present, the app raise a error 500
        try:
            access_token = data['access_token']
            email = data['email']
            username = data['username']
        except KeyError:
            return JsonResponse({'success': False, "error": "Missing required field"})

        # Optionnal
        first_name = data['first_name'] if 'first_name' in data else ''
        last_name = data['last_name'] if 'last_name' in data else ''
        avatar = data['avatar'] if 'avatar' in data else ''
        provider = data['provider'] if 'provider' in data else ''

        # Get the provider's confirmation url
        if provider in PROVIDERS.keys():
            url = PROVIDERS[provider]
        else:
            return JsonResponse({'success': False, 'error': "Unknow provider"})

        # Ask to the provider if the access_token exists and is valid
        http = httplib2.Http()
        result = http.request(url.format(access_token), 'GET')[0]

        # The provider don't return a 200 status code on error
        if result['status'] != '200':
            # The google server doesn't grant the user
            return JsonResponse({'success': False, 'error': "OAuth2 provider don't grant your identity"})

        # We don't use get_or_create because if there's more than one entry
        # an exception will be raised. Instead, we try to success silently
        # and send a signal.
        user = User.objects.filter(email=email)
        created = False

        if user.count() == 0:
            # Don't know the user.
            # Due to the email based retreiving, we seek if the username exists
            # If yes add the number of username + 1 (e.g.: paul, paul_1, paul_2, ...)
            user_username = User.objects.filter(username=username)

            if user_username.exists():
                username += "_{}".format(user_username.count() + 1)

            # Create the user
            u = User.objects.create_user(email=email, username=username, last_login=timezone.now())
            u.first_name = first_name
            u.last_name = last_name
            u.save()
            created = True

            # Create the OAuth User for authentication backend
            OAuthioUser.objects.create(user=u, provider=provider)

        elif user.count() == 1:
            # The user exists. Let's go
            user = user.get()

        else:
            # If there's a single user with two entries: there's a problem. We take
            # the first one and send a signal
            # FIXME: potential account usurpation.
            user_registration_problem.send(__name__, user=user, message="Multiple user entry.")
            user = user[0]

        auth_user = authenticate(user=user, provider=provider)
        if auth_user is None:
            user_registration_problem.send(__name__, message="An user try to authenticated with the wrong provider")
            return JsonResponse({'success': False})

        login(request, auth_user)
        oauthio_user_signin.send_robust(__name__, user=user, created=created, avatar=avatar)

        return JsonResponse({'success': True})
