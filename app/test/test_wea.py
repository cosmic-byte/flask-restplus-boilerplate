import unittest

import os
import json

from app.test.base import BaseTestCase

# Load all example API objects to be tested
script_dir = os.path.dirname(__file__)

wea = json.loads(
    open(script_dir + '/resources/weas/allahabad.json').read()
)


def create_wea(self, object_data):
    return self.client.post(
        '/wea/',
        data=json.dumps(object_data),
        content_type='application/json'
    )


def get_wea(self, object_id):
    return self.client.get(
        '/wea/' + object_id
    )


class TestEPWCRUD(BaseTestCase):
    def test_create_wea(self):
        """ Test for wea creation """
        with self.client:
            response = create_wea(self, wea)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            wea['id'] = data['id']
            response = get_wea(self, wea['id'])
            data = json.loads(response.data.decode())
            # TODO: Write better equality test to check data inside is correct
            self.assertEqual(data['id'], wea['id'])


if __name__ == '__main__':
    unittest.main()
