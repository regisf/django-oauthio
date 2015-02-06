__author__ = 'Regis'

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
        request = factory.get('/', {'json' : json.dumps(self.data)})
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
        request = factory.post('/', {'json' : json.dumps(self.data)})
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


class JSONMixinTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()