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
Authentication backend
"""

from .models import OAuthioUser


class OAuthIOBackend(object):
    def authenticate(self, user, provider):
        oauth_user = OAuthioUser.objects.filter(user=user, provider=provider)
        return oauth_user.get().user if oauth_user.exists() and oauth_user.count() == 1 else None

    def get_user(self, user_id):
        """
        return the user from the user id
        :param user_id: The user pk
        :return: The user model or none
        """
        oauth_user = OAuthioUser.objects.filter(user__id=user_id)
        if oauth_user.exists():
            return oauth_user.get().user
