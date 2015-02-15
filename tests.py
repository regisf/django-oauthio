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
Test the app
"""

__author__ = 'Regis FLORET'
__version__ = '1.0'
__license__ = 'MIT'

import json
import unittest

from django.test.client import RequestFactory

from .views import convert_request_to_json


class ConvertJsonTest(unittest.TestCase):
    data = {'one': 'test1', 'two': 'test2'}

    def test_get_empty(self):
        factory = RequestFactory()
        request = factory.get('/')
        result = convert_request_to_json(request)

        self.assertIsInstance(result, dict)
        self.assertEqual(len(result.keys()), 0)

    def test_get_exists_with_json_query(self):
        factory = RequestFactory()
        request = factory.get('/', {'json': json.dumps(self.data)})
        result = convert_request_to_json(request)

        self.assertIsInstance(result, dict)
        self.assertEqual(self.data, result)

    def test_get_query_in_body(self):
        factory = RequestFactory()
        request = factory.get('/?' + json.dumps(self.data))
        result = convert_request_to_json(request)

        self.assertIsInstance(result, dict)
        self.assertEqual(result, self.data)

    @unittest.skip('Dont know why. Digging')
    def test_post_empty(self):
        factory = RequestFactory()
        request = factory.post('/')

        convert_request_to_json(request)

    def test_post_with_json_query(self):
        factory = RequestFactory()
        request = factory.post('/', {'json': json.dumps(self.data)})
        result = convert_request_to_json(request)

        self.assertIsInstance(result, dict)
        self.assertEqual(self.data, result)

    @unittest.skip('Dont know why. Digging')
    def test_post_query_in_body(self):
        factory = RequestFactory()
        request = factory.post('/', data=self.data, format="json")
        result = convert_request_to_json(request)

        self.assertIsInstance(result, dict)
        self.assertEqual(result, self.data)


if __name__ == '__main__':
    unittest.main()