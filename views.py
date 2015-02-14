# -*- coding: UTF-8 -*-

"""
OAuth.io service for Django
(c) Régis FLORET 2015 and later

"""

__author__ = 'Regis FLORET'

import json
import httplib2

from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q

from .signals import user_signed_in, user_registration_problem


def convert_request_to_json(request):
    """ Convert a request to a json object. The request could be in the query
    http://somewhe.re/?json=[JSON.stringify object] or in the body.
    :param request: The web request
    :return The data or an empty dictionnary
    :rtype dictionnary
    """
    data = request.POST.get('json', None) if request.method == 'POST' else request.GET.get('json', None)
    data_json = None

    if data:
        data_json = json.loads(data)

    elif len(request.META['QUERY_STRING'].strip()) > 0:
        data_json = json.loads(request.META['QUERY_STRING'].replace("%22", '"'))

    elif len(request.body.strip()) > 0:
        data_json = json.loads(request.body)

    return data_json or {}


class JSONMixin(object):
    """
    The JSON View allow to respond  a json data
    """

    def get(self, request):
        return HttpResponse(
            json.dumps(
                self.get_data(request, convert_request_to_json(request)),
                ensure_ascii=False
            ),
            content_type="application/json"
        )

    def post(self, request):
        return HttpResponse(
            json.dumps(
                self.post_data(request, convert_request_to_json(request)),
                ensure_ascii=False
            ),
            content_type="application/json"
        )

    def get_data(self, request, data):
        raise NotImplementedError("This method might be implemented")

    def post_data(self, request, data):
        raise NotImplementedError('This method might be implemented')


PROVIDERS = {
    'facebook': 'https://graph.facebook.com/me?fields=id&access_token={}',
    'google_plus': 'https://www.googleapis.com/plus/v1/people/me?access_token={}',
    'linkedin': 'https://api.linkedin.com/v1/people/~?oauth2_access_token={}&format=json',
    'twitter': 'https://api.twitter.com/oauth/access_token',
    'yahoo': 'http://social.yahooapis.com/v1/user/{}/profile?format=json',
    #'live': ''
}


class ConnectSocialView(JSONMixin, View):
    """

    """
    def get_data(self, request, data):
        """
        Avoid IDE claims
        """
        super(ConnectSocialView, self).get(request)

    def post_data(self, request, data):
        access_token = data['access_token']
        email = data['email'] if 'email' in data else None
        username = data['name'] if 'name' in data else None
        first_name = data['first_name'] if 'first_name' in data else ''
        last_name = data['last_name'] if 'last_name' in data else ''
        avatar = data['avatar'] if 'avatar' in data else ''
        provider = data['provider'] if 'provider' in data else None

        if provider in PROVIDERS.keys():
            url = PROVIDERS[provider]
        else:
            return {'success': False, 'error': "Unknow provider"}

        http = httplib2.Http()
        result = http.request(url.format(access_token), 'GET')[0]

        if result['status'] != '200':
            # The google server doesn't grant the user
            return {'success': False, 'error': "OAuth2 provider don't grant your identity"}

        # We don't use get_or_create because if there's more than one entry
        # an exception will be raised. Instead, we try to success silently
        # and send a signal.
        user = User.objects.filter(Q(email=email))
        created = user.count() == 0

        if user.count() == 0:
            # Don't know the user.
            # Due to the email based retreiving, we seek if the username exists
            # If yes add the number of username + 1 (e.g.: paul, paul_1, paul_2, ...)
            user_username = User.objects.filter(username__iregex=r'^{}'.format(username))
            if user_username.exists():
                username += "_{}".format(user_username.count() + 1)

            # Create the user
            u = User.objects.create_user(email=email, username=username)
            u.first_name = first_name
            u.last_name = last_name
            u.save()
            created = True

        elif user.count() == 1:
            # The user exists. Let's go
            user = user.get()

        else:
            # If there's a single user with two entries: there's a problem. We take
            # the first one and send a signal
            # FIXME: potential account usurpation.
            user_registration_problem.send(sender=self, user=user, message="Multiple user entry.")
            user = user[0]

        user_signed_in.send(sender=self, user=user, created=created, avatar=avatar)

        return {'success': True}