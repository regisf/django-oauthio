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
Model for users authenticated with social network
"""

__author__ = 'Regis FLORET'
__version__ = '1.0'
__license__ = 'MIT'

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class OAuthioUser(models.Model):
    """
    This model is by the authentication backend.
    see ./backend.py
    """

    # Django user assocation
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        help_text=_("The django framework username"),
        db_index=True
    )

    # From which social network did the user come
    provider = models.CharField(
        max_length=20,
        verbose_name=_("Provider"),
        help_text=_("From which Social network the user comes")
    )

    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = "oauthio_oauthiouser"
